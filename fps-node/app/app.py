import time
import json
import socket
import requests
import threading

from flask import Flask, render_template


class FpsCalculator():
    """Helper class for calculating frames-per-second (FPS)."""

    def __init__(self, decay_factor=0.95):
        self.fps = 0.0
        self.tic = time.time()
        self.decay_factor = decay_factor

    def update(self):
        toc = time.time()
        curr_fps = 1.0 / (toc - self.tic)
        self.fps = curr_fps if self.fps == 0.0 else self.fps
        self.fps = self.fps * self.decay_factor + \
                   curr_fps * (1 - self.decay_factor)
        self.tic = toc
        return self.fps

    def reset(self):
        self.fps = 0.0


local_docker_network_ip = None
cached_response = { "message": "Empty" }


def get_target():
    global local_docker_network_ip
    if (not local_docker_network_ip):
        local_docker_network_ip = socket.gethostbyname(socket.gethostname())    
    subnet_mask = local_docker_network_ip[:-2]
    target = subnet_mask + ".0" + str(3)
    return target


class GetThread(threading.Thread):
    """GetThread

    This thread bangs and issues GET towards the upstream Container, in
    order to measure the maximum FPS achieved by the pipeline (proceeding
    this Fps Node).
    """

    def __init__(self):
        super().__init__()
        self.fps_calc = FpsCalculator()
        self.running = False

    def run(self):
        global cached_response
        self.running = True
        while self.running:
            # Try to GET again as soon as we receive response from the
            # previous GET
            try:
                upstream_container = f"http://{get_target()}:8080/get"
                response = requests.get(upstream_container)
                if response.status_code == 200:
                    j = response.json()
                    j["fps"] = self.fps_calc.update()
                    cached_response = j
            except Exception as e:
                print(e)

    def stop(self):
        self.running = False
        self.join()


app = Flask(__name__)


@app.route("/get")
def get():
    return app.response_class(
        response=json.dumps(cached_response),
        status=200,
        mimetype='application/json')


if __name__ == "__main__":
    get_thread = GetThread()
    get_thread.start()
    app.run(debug=False, host='0.0.0.0', port=8080)
    get_thread.stop()

import time
import json
import socket
import requests

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


fps_calc = FpsCalculator()
local_docker_network_ip = None
app = Flask(__name__)


def get_target():
    global local_docker_network_ip
    if (not local_docker_network_ip):
        local_docker_network_ip = socket.gethostbyname(socket.gethostname())    
    subnet_mask = local_docker_network_ip[:-2]
    target = subnet_mask + ".0" + str(3)
    return target


@app.route("/get")
def get():
    try:
        upstream_container = f"http://{get_target()}:8080/get"
        response = requests.get(upstream_container)
        if response.status_code == 200:
            j = response.json()
            j["fps"] = fps_calc.update()
            return app.response_class(
                response=json.dumps(j),
                status=200,
                mimetype='application/json')
    except Exception as e:
        print(e)


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=8080)

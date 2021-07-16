FROM alpine:3.13

LABEL maintainer="JK Jung" \
      email="jkjung13@gmail.com"

RUN apk update
RUN apk add --no-cache python3 py3-pip

COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN pip3 install -r requirements.txt

COPY . /

EXPOSE 8080 8080

ENTRYPOINT [ "python3" ]

CMD [ "/app/app.py" ]

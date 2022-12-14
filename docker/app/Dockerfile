FROM python:3.9.13-slim-bullseye

RUN mkdir /app
WORKDIR /app
ADD app /app/
RUN python3 -m pip install -r /app/requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

ENV BALANCER_URL=http://balancer:8081
WORKDIR "/"
CMD ["python3", "-m", "app"]

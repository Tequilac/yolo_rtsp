FROM python:3.9.13-slim-bullseye

RUN mkdir /balancer
WORKDIR /balancer
ADD balancer /balancer/
RUN python3 -m pip install -r /balancer/requirements.txt

ENV PYTHONUNBUFFERED=1
EXPOSE 8081
WORKDIR "/"
CMD ["python3", "-m", "balancer"]

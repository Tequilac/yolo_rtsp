FROM python:3.9.13-slim-bullseye

RUN mkdir /balancer
WORKDIR /balancer
ADD balancer /balancer/
RUN python3 -m pip install -r /balancer/requirements.txt

EXPOSE 8081
CMD ["python3", "-m", "balancer"]

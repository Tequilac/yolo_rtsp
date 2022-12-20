FROM python:3.9.13-slim-bullseye

RUN mkdir /app
WORKDIR /app
ADD app /app/
RUN python3 -m pip install --no-cache-dir --no-compile -r /app/requirements.txt

ENV PYTHONUNBUFFERED=1
ENV BALANCER_URL=http://balancer:8081
WORKDIR "/"
CMD ["python3", "-m", "app"]

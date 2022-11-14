FROM python:3.9.13-slim-bullseye

RUN mkdir /app
WORKDIR /app
ADD app /app/
RUN python3 -m pip install -r /app/requirements.txt


EXPOSE 5000
CMD ["python3", "-m", "app"]

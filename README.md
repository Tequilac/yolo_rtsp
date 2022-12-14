# YOLO RTSP

This is a project for running a yolo object detection on a continuous stream of data read with the RTSP protocol
and sending the result data on an MQTT topic.

## Project structure

The project consists of:
* **balancer** - a balancer application which manages config for all the streams to be analyzed. 
  The config can be provided in the `conf.yaml` in the resources and can also be changed in runtime by using an API endpoint.
* **app** - the application that analyzes the stream based on a config it gets from the balancer application.
If the config provided to the balancer changes, the app will notice it and reload.
  
For the system to work there needs to be exactly one instance of balancer and at least one instance of the app running.

## Structure of the streams config

The streams' config must be provided in a specific format (here presented as a yaml from the `conf.yaml` file,
for accessing the endpoint the config should be a json):
```yaml
---
streams: # list of the configs for streams
  - frame_rate_timeout: [float] # timeout between reading next frame to be analyzed
    rtsp_url: [string] # url of the rtsp stream to be read
    frame_strategy: [DROP or STORE] # strategy for managing frames (see below)
    mqtt_info: # mqtt channel info to send results to (on connection fais the info will be logged)
      client_id: [string]
      username: [string]
      password: [string]
      broker: [string]
      port: [int]
      topic: [string]
```

### Frame strategy

THere are two possible strategies for frames if the previous one hasn't finished being analyzed in the provided timeout:
* DROP - the new frame is dropped 
  (preferred if the frames should be analyzed as fast as possible at the expense of not analyzing every frame if it takes some time)
* STORE - the new frame is stored and will start to be analyzed once the previous one finishes being analyzed
  (preferred if every frame should be eventually analyzed)

## Running the project

### Locally

Run the balancer:
```shell
python -m balancer
```
Run the app:
```shell
export BALANCER_URL=http://localhost:8081
python -m app
```

### In Docker container

Use the files provided in the `docker` directory to build the container images.

For building on the arm64 architecture first use:
```shell
sudo apt install -y qemu-user-static binfmt-support
docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
docker buildx create --name profile
docker buildx use profile
docker buildx inspect --bootstrap
```
Build the balancer:
```shell
sudo docker buildx build --platform linux/arm64 -t tequilac/balancer -f docker/balancer/Dockerfile --push .
```
Build the app:
```shell
sudo docker buildx build --platform linux/arm64 -t tequilac/app -f docker/app/Dockerfile --push .
```

### On Kubernetes cluster

Use the files provided in the `deployment` directory.
Note that the images specified for the deployments were built for arm64 architecture.


### YOLO network

To use the YOLO object detection please place the following files in the `app/res/files` directory:
* https://pjreddie.com/media/files/yolov3.weights
* https://github.com/arunponnusamy/object-detection-opencv/blob/master/yolov3.cfg
* https://github.com/arunponnusamy/object-detection-opencv/blob/master/yolov3.txt



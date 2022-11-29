import yaml

from .types import Config, FrameStrategy, MqttInfo, Stream


def conf_from_obj(conf) -> Config:
    streams = conf['streams']
    streams_conf = []
    for stream in streams:

        info = stream['mqtt_info']
        mqtt_info = MqttInfo(
            client_id=info['client_id'], username=info['username'], password=info['password'],
            broker=info['broker'], port=info['port'], topic=info['topic']
        )
        streams_conf.append(Stream(
            frame_rate_timeout=stream['frame_rate_timeout'], rtsp_url=stream['rtsp_url'],
            mqtt_info=mqtt_info, frame_strategy=FrameStrategy[stream['frame_strategy']].name,
        ))
    return Config(streams=streams_conf)


def load_from_file():
    file_path = '/balancer/res/config/conf.yaml'
    with open(file_path, 'r') as stream:
        conf = yaml.safe_load(stream)
    return conf

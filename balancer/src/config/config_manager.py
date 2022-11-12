from .types import Config, FrameStrategy, MqttInfo, Stream
import yaml

from ..streams.streams_manager import StreamsManager


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
            frame_rate_timeout=conf['frame_rate_timeout'], rtsp_url=conf['rtsp_url'],
            mqtt_info=mqtt_info, frame_strategy=FrameStrategy[conf['frame_strategy']],
        ))
    return Config(streams=streams_conf)


def load_from_file():
    file_path = 'app\\res\\config\\conf.yaml'
    with open(file_path, 'r') as stream:
        conf = yaml.safe_load(stream)
    return conf


class ConfigManager:

    def __init__(self) -> None:
        self._streams_manager = None
        self.reload_config(load_from_file())

    def reload_config(self, conf):
        config = conf_from_obj(conf)
        self._streams_manager = StreamsManager(config)

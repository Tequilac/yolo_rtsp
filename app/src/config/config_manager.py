import json
import os
import uuid

import requests

from .status import Request, Status
from .types import Config, FrameStrategy, MqttInfo
from ..frames.frames_manager import FramesManager
from ..frames.rtsp_reader import RtspReader
import yaml


def conf_from_obj(conf) -> Config:
    info = conf['mqtt_info']
    mqtt_info = MqttInfo(
        client_id=info['client_id'], username=info['username'], password=info['password'],
        broker=info['broker'], port=info['port'], topic=info['topic']
    )
    return Config(
        frame_rate_timeout=conf['frame_rate_timeout'], rtsp_url=conf['rtsp_url'],
        mqtt_info=mqtt_info, frame_strategy=FrameStrategy[conf['frame_strategy']]
    )


def load_from_file():
    file_path = 'app\\res\\config\\conf.yaml'
    with open(file_path, 'r') as stream:
        conf = yaml.safe_load(stream)
    return conf


class ConfigManager:

    def __init__(self) -> None:
        self._id = uuid.uuid4()
        self._balancer_url = os.environ['BALANCER_URL']
        self._has_config = False
        self._frames_manager = None
        self._rtsp_reader = None
        self._mqtt_info = None
        self._rtsp_url = None
        self._frame_rate = None
        self.reload_config(load_from_file())



    def check_for_config_reload(self):
        status = Status.BUSY if self._has_config else Status.READY
        response = requests.get(self._balancer_url, json=json.dumps(Request(status=status, app_id=self._id)))

    def reload_config(self, conf):
        config = get_config(conf)
        if self._rtsp_reader:
            self._rtsp_reader.stop_capture()
        if self._frames_manager:
            self._frames_manager.stop()
        self._frames_manager = FramesManager(config.frame_strategy, config.mqtt_info)
        self._rtsp_reader = RtspReader(config.frame_rate_timeout, config.rtsp_url, self._frames_manager)

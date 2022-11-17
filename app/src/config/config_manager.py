import json
import os
import time
import uuid
from typing import cast

import requests

from .status import Request, Status, Response, Keep, Ditch, New
from .types import Config, FrameStrategy, MqttInfo
from ..frames.frames_manager import FramesManager
from ..frames.rtsp_reader import RtspReader


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


def response_from_obj(resp) -> Response:
    operation_name = resp['operation']['name']
    if operation_name == 'KEEP':
        return Response(operation=Keep())
    elif operation_name == 'DITCH':
        return Response(operation=Ditch())
    elif operation_name == 'NEW':
        conf = resp['operation']['config']
        return Response(operation=New(config=conf_from_obj(conf)))


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
        self.start_pooling_for_config_reload()

    def start_pooling_for_config_reload(self):
        while True:
            self.request_for_config()
            time.sleep(10)

    def request_for_config(self):
        status = Status.BUSY if self._has_config else Status.READY
        request = Request(status=status, app_id=self._id)
        resp = requests.get(self._balancer_url, json=json.dumps(request))
        if resp.ok:
            obj = json.loads(resp.json())
            operation = response_from_obj(obj).operation
            if operation.name == 'KEEP':
                return
            elif operation.name == 'DITCH':
                self.ditch_current()
            elif operation.name == 'NEW':
                self.reload_config(cast(operation, New).config)

    def ditch_current(self):
        self._frames_manager = None
        self._rtsp_reader = None

    def reload_config(self, config: Config):
        if self._rtsp_reader:
            self._rtsp_reader.stop_capture()
        if self._frames_manager:
            self._frames_manager.stop()
        self._frames_manager = FramesManager(config.frame_strategy, config.mqtt_info)
        self._rtsp_reader = RtspReader(config.frame_rate_timeout, config.rtsp_url, self._frames_manager)

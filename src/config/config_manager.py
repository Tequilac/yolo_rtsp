from .types import Config, FrameStrategy
from ..frames.frames_manager import FramesManager
from ..frames.rtsp_reader import RtspReader


class ConfigManager:

    def __init__(self) -> None:
        self._frames_manager = None
        self._rtsp_reader = None
        self._mqtt_info = None
        self._rtsp_url = None
        self._frame_rate = None
        self.reload_config(Config(frame_rate=30, rtsp_url='', mqtt_info=None, frame_strategy=FrameStrategy.DROP))

    def reload_config(self, config: Config):
        if self._rtsp_reader:
            self._rtsp_reader.stop_capture()
        if self._frames_manager:
            self._frames_manager.stop()
        self._frames_manager = FramesManager(config['frame_strategy'], config['mqtt_info'])
        self._rtsp_reader = RtspReader(config['frame_rate'], config['rtsp_url'], self._frames_manager)

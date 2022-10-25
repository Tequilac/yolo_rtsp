from .types import Config, FrameStrategy


class ConfigManager:

    def __init__(self) -> None:
        self._mqtt_info = None
        self._rtsp_url = None
        self._frame_rate = None
        self.reload_config(Config(frame_rate=30, rtsp_url='', mqtt_info=None, frame_strategy=FrameStrategy.DROP))

    def reload_config(self, config: Config):
        self._frame_rate = config['frame_rate']
        self._rtsp_url = config['rtsp_url']
        self._mqtt_info = config['mqtt_info']

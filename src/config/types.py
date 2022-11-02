from typing import TypedDict


class FrameStrategy:
    DROP = 0
    STORE = 1


class MqttInfo(TypedDict):
    address: str
    topic: str


class Config(TypedDict):
    frame_rate: int
    rtsp_url: str
    mqtt_info: MqttInfo
    frame_strategy: FrameStrategy

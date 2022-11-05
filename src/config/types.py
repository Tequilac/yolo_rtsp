from typing import TypedDict


class FrameStrategy:
    DROP = 0
    STORE = 1


class MqttInfo(TypedDict):
    client_id: str
    username: str
    password: str
    broker: str
    port: int
    topic: str


class Config(TypedDict):
    frame_rate: int
    rtsp_url: str
    mqtt_info: MqttInfo
    frame_strategy: FrameStrategy

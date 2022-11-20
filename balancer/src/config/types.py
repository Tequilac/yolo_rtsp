from dataclasses import dataclass
from enum import Enum


class FrameStrategy(Enum):
    DROP = 'DROP'
    STORE = 'STORE'


@dataclass
class MqttInfo:
    client_id: str
    username: str
    password: str
    broker: str
    port: int
    topic: str


@dataclass
class Stream:
    frame_rate_timeout: float
    rtsp_url: str
    mqtt_info: MqttInfo
    frame_strategy: str


@dataclass
class Config:
    streams: list[Stream]

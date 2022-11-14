from datetime import datetime
import uuid
from dataclasses import dataclass
from enum import Enum

from balancer.src.config.types import Stream


class StreamStatus:
    name: str


class Free(StreamStatus):
    name = 'FREE'


class Taken(StreamStatus):
    name = 'TAKEN'
    app_id: uuid.UUID


@dataclass
class Active:
    app_id: uuid.UUID
    last_contact_time: datetime
    stream_hash: str


class Status(Enum):
    READY = 'READY'
    BUSY = 'BUSY'


@dataclass
class Request:
    status: Status
    app_id: uuid.UUID


@dataclass
class Operation:
    pass


@dataclass
class Keep(Operation):
    name = 'KEEP'


@dataclass
class Change(Operation):
    name = 'CHANGE'


@dataclass
class New(Operation):
    name = 'NEW'
    config: Stream


@dataclass
class Response:
    operation: Operation

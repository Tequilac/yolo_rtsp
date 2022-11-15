import uuid
from dataclasses import dataclass
from enum import Enum

from app.src.config.types import Config


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
class Ditch(Operation):
    name = 'DITCH'


@dataclass
class New(Operation):
    name = 'NEW'
    config: Config


@dataclass
class Response:
    operation: Operation

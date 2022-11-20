import uuid
from dataclasses import dataclass
from enum import Enum

from app.src.config.types import Config


class Status(Enum):
    READY = 'READY'
    BUSY = 'BUSY'


@dataclass
class Request:
    status: str
    app_id: uuid.UUID


@dataclass
class Operation:
    name: str


@dataclass
class Keep(Operation):
    name: str = 'KEEP'


@dataclass
class Ditch(Operation):
    name: str = 'DITCH'


@dataclass
class New(Operation):
    name: str = 'NEW'
    config: Config = None


@dataclass
class Response:
    operation: Operation

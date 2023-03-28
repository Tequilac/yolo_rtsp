from datetime import datetime
from dataclasses import dataclass


@dataclass
class FrameInfo:
    frame: object
    timestamp: datetime

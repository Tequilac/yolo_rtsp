from datetime import datetime
from dataclasses import dataclass

import numpy as np


@dataclass
class FrameInfo:
    frame: np.ndarray
    timestamp: datetime

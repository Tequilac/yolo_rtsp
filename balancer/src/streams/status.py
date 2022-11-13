from datetime import datetime
import uuid
from dataclasses import dataclass


@dataclass
class Active:
    app_id: uuid.UUID
    last_contact_time: datetime

class Status:
    READY = 'READY'


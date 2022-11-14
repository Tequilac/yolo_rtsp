import uuid
from typing import cast

from balancer.src.config.types import Config
from balancer.src.streams.status import StreamStatus, Free, Taken


class StreamsManager:
    def __init__(self, config: Config):
        self._config = config
        self._statuses = list[StreamStatus]([Free() for _ in range(len(self._config.streams))])

    def get_new_stream(self, app_id: uuid.UUID):
        for idx, status in enumerate(self._statuses):
            if status.name == 'FREE':
                return self._config.streams[idx]

    def check_for_change(self, app_id: uuid.UUID):
        for idx, status in enumerate(self._statuses):
            if status.name == 'TAKEN':
                if cast(Taken, status).app_id == app_id:
                    return self._config.streams[idx]

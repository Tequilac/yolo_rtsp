from datetime import datetime
import uuid
from typing import cast

from balancer.src.config.types import Config
from balancer.src.streams.status import StreamStatus, Free, Taken, Active


class StreamsManager:
    def __init__(self, config: Config):
        self._config = config
        self._statuses: list[StreamStatus] = ([Free() for _ in range(len(self._config.streams))])
        self._active_apps: list[Active] = []

    def update_active(self, app_id: uuid.UUID):
        found = False
        for app in self._active_apps:
            if app.app_id == app_id:
                app.last_contact_time = datetime.now()
                found = True
        if not found:
            self._active_apps.append(Active(app_id=app_id, last_contact_time=datetime.now()))
        self.ditch_inactive()

    def ditch_inactive(self):
        current_time = datetime.now()
        to_be_ditched = []
        for idx, app in enumerate(self._active_apps):
            if (current_time - app.last_contact_time).seconds > 30:
                to_be_ditched.append(app.app_id)
        self.ditch_apps(to_be_ditched)

    def ditch_apps(self, app_ids: list[uuid.UUID]):
        for idx, status in enumerate(self._statuses):
            if status.name == 'TAKEN':
                if cast(Taken, status).app_id in app_ids:
                    self._statuses[idx] = Free()
        self._active_apps = [x for x in self._active_apps if x.app_id not in app_ids]

    def get_new_stream(self, app_id: uuid.UUID):
        for idx, status in enumerate(self._statuses):
            if status.name == 'FREE':
                self._statuses[idx] = Taken(app_id=app_id)
                return self._config.streams[idx]
        return None

    def check_for_change(self, app_id: uuid.UUID):
        for idx, status in enumerate(self._statuses):
            if status.name == 'TAKEN':
                if cast(Taken, status).app_id == app_id:
                    return False, None
        new = self.get_new_stream(app_id)
        if new:
            return True, new
        return True, None

from uuid import UUID

from balancer.src.config.config_utils import conf_from_obj, load_from_file
from balancer.src.streams.status import Request, Status
from balancer.src.streams.streams_manager import StreamsManager


def request_from_json(req):
    return Request(status=Status[req['status']], app_id=UUID(req['app_id']))


class StreamsService:
    def __init__(self):
        self._streams_manager = StreamsManager(load_from_file())

    def reload_config(self, config):
        conf = conf_from_obj(config)
        self._streams_manager = StreamsManager(conf)

    def handle_request(self, req):
        request = request_from_json(req)
        if request.status == Status.READY:
            self._streams_manager.get_new_stream(request.app_id)
        elif request.status == Status.BUSY:
            self._streams_manager.check_for_change(request.app_id)

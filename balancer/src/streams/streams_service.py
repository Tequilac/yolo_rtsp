from uuid import UUID

from balancer.src.config.config_utils import conf_from_obj, load_from_file
from balancer.src.logger import logger
from balancer.src.streams.status import Request, Status, Response, Keep, New, Ditch
from balancer.src.streams.streams_manager import StreamsManager


def request_from_json(req):
    return Request(status=Status[req['status']], app_id=UUID(req['app_id']))


class StreamsService:
    def __init__(self):
        self._streams_manager = StreamsManager(conf_from_obj(load_from_file()))

    def reload_config(self, config):
        conf = conf_from_obj(config)
        logger.info(f'Reloading config to: {conf}')
        self._streams_manager = StreamsManager(conf)

    def handle_request(self, req):
        request = request_from_json(req)
        logger.info(f'Received request: {request}')
        self._streams_manager.update_active(request.app_id)
        if request.status == Status.READY:
            stream = self._streams_manager.get_new_stream(request.app_id)
            if stream:
                operation = New(config=stream)
            else:
                operation = Keep()
            return Response(operation=operation)
        elif request.status == Status.BUSY:
            should_change, stream = self._streams_manager.check_for_change(request.app_id)
            if should_change:
                if stream:
                    operation = New(config=stream)
                else:
                    operation = Ditch()
            else:
                operation = Keep()
            return Response(operation=operation)

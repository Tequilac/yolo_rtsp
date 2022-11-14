import json

from flask import Response

from balancer.src.streams.streams_service import StreamsService


class StreamsCaller:
    def __init__(self, streams_service: StreamsService):
        self._streams_service = streams_service
        self.response = Response(status=200, headers={})

    def __call__(self, *args):
        params = json.loads(args[0])
        self._streams_service.handle_request(params)
        return self.response

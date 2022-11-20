import json

from flask import Response, request

from ..streams.streams_service import StreamsService


class ConfigReloader:
    def __init__(self, streams_service: StreamsService):
        self._streams_service = streams_service
        self.response = Response(status=200, headers={})

    def __call__(self, *args):
        params = json.loads(request.json)
        self._streams_service.reload_config(params)
        return self.response

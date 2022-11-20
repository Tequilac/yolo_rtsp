import json

from flask import Response, request

from balancer.src.streams.streams_service import StreamsService


class StreamsCaller:
    def __init__(self, streams_service: StreamsService):
        self._streams_service = streams_service
        self.response = Response(status=200, headers={})

    def __call__(self, *args):
        print('Received request: ' + request.json)
        params = json.loads(request.json)
        resp = self._streams_service.handle_request(params)
        print(resp)
        return Response(status=200, headers={}, response=json.dumps(resp, default=lambda o: o.__dict__))

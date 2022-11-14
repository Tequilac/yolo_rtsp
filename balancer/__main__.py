from .src.streams.streams_caller import StreamsCaller
from .src.streams.streams_service import StreamsService
from .src.config.config_reloader import ConfigReloader
from .src.flask_app_wrapper import FlaskAppWrapper


if __name__ == "__main__":
    app = FlaskAppWrapper(__name__)
    streams_service = StreamsService()
    app.add_endpoint(endpoint='/config', endpoint_name='config', handler=ConfigReloader(streams_service))
    app.add_endpoint(endpoint='/streams', endpoint_name='streams', handler=StreamsCaller(streams_service))
    app.run()

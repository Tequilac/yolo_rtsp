from balancer.src.config.types import Config


class StreamsManager:
    def __init__(self, config: Config):
        self._config = config
        self._statuses = []

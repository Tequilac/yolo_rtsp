import json

from flask import Response

from .config_manager import ConfigManager


class ConfigReloader:
    def __init__(self, config_manager: ConfigManager):
        self._config_manager = config_manager
        self.response = Response(status=200, headers={})

    def __call__(self, *args):
        params = json.loads(args[0])
        self._config_manager.reload_config(params)
        return self.response

from .src.config.config_manager import ConfigManager
from .src.config.config_reloader import ConfigReloader
from .src.flask_app_wrapper import FlaskAppWrapper


if __name__ == "__main__":
    app = FlaskAppWrapper(__name__)
    app.add_endpoint(endpoint='/config', endpoint_name='config', handler=ConfigReloader(ConfigManager()))
    app.run()

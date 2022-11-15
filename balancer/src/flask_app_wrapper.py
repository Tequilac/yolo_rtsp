from flask import Flask


class FlaskAppWrapper:
    app = None

    def __init__(self, name):
        self.app = Flask(name)

    def run(self):
        self.app.run(host='0.0.0.0', port=8081)

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None):
        self.app.add_url_rule(endpoint, endpoint_name, handler)

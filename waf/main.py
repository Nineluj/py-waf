import logging

import click
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from waf.modules.security_headers import SecurityHeaders
from .helper import parse_config
from .reverse_proxy import reverse_proxy

app = Flask(__name__)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["5000/day", "500/hour"]
)
USAGE = "Run with --help for options"
app.register_blueprint(reverse_proxy)


@click.command()
@click.option('--config-path', '-c', help='Path to config file', metavar='PATH')
def main(config_path) -> None:
    """Read the config"""
    if not config_path:
        print(USAGE)
        exit(1)

    parse_config(config_path, app)

    # Set up the app
    if app.config['debug']:
        app.logger.setLevel(logging.DEBUG)

    # Set up SSL if configured to
    security_context = None

    if app.config['use_ssl']:
        cert = app.config['ssl_cert']
        key = app.config['ssl_key']
        security_context = (cert, key)

    SecurityHeaders(app)()

    app.run(host='0.0.0.0', port=app.config['port'], debug=app.config['debug'], ssl_context=security_context)

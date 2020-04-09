import logging

import click
from flask import Flask

from waf.modules.rate_limiter import RateLimiter
from waf.modules.security_headers import SecurityHeaders
from .helper import parse_config
from .reverse_proxy import reverse_proxy

app = Flask(__name__)

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

    """Run the general modules"""
    SecurityHeaders(app)()
    RateLimiter(app)()

    app.run(host='0.0.0.0', port=app.config['port'], debug=app.config['debug'], ssl_context=security_context)

import logging
from ssl import SSLContext

import click
from flask import Flask
from gevent.pywsgi import WSGIServer
from werkzeug.debug import DebuggedApplication

from waf.modules.rate_limiter import RateLimiter
from waf.modules.security_headers import SecurityHeaders
from .helper import parse_config
from .reverse_proxy import reverse_proxy


@click.command()
@click.option('--config-path', '-c', help='Path to config file', metavar='PATH', envvar='CONFIG_PATH')
def main(config_path):
    # Static directory can be changed here to avoid collisions with underlying app's static directory
    app = Flask(__name__)

    USAGE = "Run with --help for options"
    app.register_blueprint(reverse_proxy)

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
        security_context = SSLContext()
        security_context.load_cert_chain(cert, key)

    """Run the general modules"""
    SecurityHeaders(app)()
    RateLimiter(app)()

    app.logger.info(f"pyWaf running at 0.0.0.0:{app.config['port']}")
    http_server = WSGIServer(('0.0.0.0', app.config['port']), DebuggedApplication(app) if app.config['debug'] else app,
                             ssl_context=security_context)
    http_server.serve_forever()

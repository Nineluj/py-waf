import click
import logging

from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman

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

    config = parse_config(config_path, app)

    # Set up the app
    if config['debug']:
        app.logger.setLevel(logging.DEBUG)

    app.logger.debug(f'Loaded config as {config}')

    # Set up SSL if configured to
    security_context = None

    if config['use_ssl']:
        cert = config['ssl_cert']
        key = config['ssl_key']
        security_context = (cert, key)

    """Safe defaults for security headers"""
    security_headers_flag = config['modules'].pop('security_headers', True)
    if security_headers_flag:
        """Read this from config actually. This config is quite unsafe but it is here to make the vuln-app work."""
        Talisman(app, content_security_policy={
            'default-src': '\'self\'',
            'style-src': ['\'unsafe-inline\'', '\'self\''],
            'script-src': ['\'self\'', '\'unsafe-inline\'']
        })

    app.run(host='0.0.0.0', port=config['port'], debug=config['debug'], ssl_context=security_context)

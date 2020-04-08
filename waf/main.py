import click
import logging

from flask import Flask
from .helper import parse_config
from .reverse_proxy import reverse_proxy


app = Flask(__name__)
USAGE = "Run with --help for options"
app.register_blueprint(reverse_proxy)


@app.route('/hello')
def index() -> str:
    return 'Hello'


@click.command()
@click.option('--config-path', '-c', help='Path to config file', metavar='PATH')
def main(config_path) -> None:
    """Read the config"""
    if not config_path:
        print(USAGE)
        exit(1)

    config = parse_config(config_path)

    # Copy the config key-pair values to the app config to make them accessible
    # in other places.
    for k, v in config.items():
        app.config[k] = v

    # Set up the app
    if config['debug']:
        logging.basicConfig(level=logging.DEBUG)

    logging.debug(f'Loaded config as {config}')

    # Set up SSL if configured to
    security_context = None

    if config['use_ssl']:
        cert = config['ssl_cert']
        key = config['ssl_key']
        security_context = (cert, key)

    app.run(host='0.0.0.0', port=config['port'], debug=config['debug'], ssl_context=security_context)

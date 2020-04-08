import click
import logging

from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
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

    if config['debug']:
        logging.basicConfig(level=logging.DEBUG)

    logging.debug(f'Loaded config as {config}')

    # Copy the config key-pair values to the app config to make them accessible
    # in other places.
    for k, v in config.items():
        app.config[k] = v

    app.run(host='0.0.0.0', port=config['port'], debug=config['debug'])

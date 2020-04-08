import click
from flask import Flask
import logging

from src.helper import parse_config

USAGE = "Run with --help for options"
app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello'


@click.command()
@click.option('--config', help='Path to config file', metavar='PATH')
def main(config_path):
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

    app.run(port=config['port'], debug=config['debug'])

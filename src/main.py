import click
from flask import Flask
import logging

from .helper import parse_config

USAGE = "Run with --help for options"

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello'

@click.command()
@click.option('--config', help='Path to config file', metavar='PATH')
def main(config):
    """Read the config"""
    if not config:
        print(USAGE)
        exit(1)

    config = parse_config(config)

    if config['debug']:
        logging.basicConfig(level=logging.DEBUG)

    logging.debug(f'Loaded config as {config}')

    app.run(port=config['port'], debug=config['debug'])

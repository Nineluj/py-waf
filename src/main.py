import click
from flask import Flask
import logging

from helper import parse_config

USAGE = "Run with --help for options"
app = Flask(__name__)


@app.route('/hello')
def index():
    return 'Hello'


@click.command()
@click.option('--config', '-c', help='Path to config file', metavar='PATH')
def main(config_path):
    """Read the config"""
    if not config_path:
        print(USAGE)
        exit(1)

    config = parse_config(config_path)

    if config['debug']:
        logging.basicConfig(level=logging.DEBUG)

    logging.debug(f'Loaded config as {config}')

    app.run(port=config['port'], debug=config['debug'])

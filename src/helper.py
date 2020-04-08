from yaml import safe_load
import logging


def parse_config(config: str) -> object:
    """
    Load the config from the provided path and return it.
    """
    config = safe_load(open(config))
    REQUIRED_KEYS = [
        'server_addr',
        'port'
    ]
    OPTIONAL_KEYS = {
        'debug': False
    }

    for k in REQUIRED_KEYS:
        if k not in config:
            raise Exception(f'config needs a {k} field')

    for k in OPTIONAL_KEYS:
        if k not in config:
            config[k] = OPTIONAL_KEYS[k]

    return config

from yaml import safe_load
import logging


def parse_config(config_path: str, app) -> object:
    """
    Load the config from the provided path and return it.
    """
    config = safe_load(open(config_path))
    REQUIRED_KEYS = [
        'server_addr',
        'port'
    ]
    OPTIONAL_KEYS = {
        'debug': False,
        'modules': {}
    }

    for k in REQUIRED_KEYS:
        if k not in config:
            raise Exception(f'config needs a {k} field')

    for k in OPTIONAL_KEYS:
        if k not in config:
            config[k] = OPTIONAL_KEYS[k]

    # Copy the config key-pair values to the app config to make them accessible
    # in other places.
    for k, v in config.items():
        app.config[k] = v

    return config

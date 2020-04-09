from yaml import safe_load
from flask import render_template, render_template_string


REASON_CONTENT_FILTER = "PyWAF has blocked this request because of it's content filter."
REASON_UNEXPECTED = "PyWAF was not able to complete this request for an unexpected reason."


def make_error_page(code: int, additional: str, unexpected=False):
    """Returns a rendered template with error code to display error. unexpected should be set if the
    error happened because of an error rather than an attempted attack"""
    reason = REASON_UNEXPECTED if unexpected else REASON_CONTENT_FILTER

    return render_template("/error.html",
                           reason=reason,
                           additional=additional,
                           statuscode=code), code


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

from enum import Enum

from flask import escape
from werkzeug.datastructures import MultiDict
from werkzeug.urls import url_encode

from waf.exceptions.xss_exception import XSSException
from waf.helper import make_error_page

"""
XSS Checks
"""


class Mode(Enum):
    MITIGATE = 0
    BLOCK = 1


class XSSCheck(object):
    def __init__(self, app):
        self.app = app
        self.enabled = (app.config['modules'].get('xss', {'enabled': True})).get('enabled', True)
        self.mode = Mode((app.config['modules'].get('xss', {'mode': 0})).get('mode', 0))
        supported_modes = {Mode.MITIGATE, Mode.BLOCK}
        if self.mode not in supported_modes:
            self.mode = Mode.MITIGATE

    def __call__(self, args: MultiDict):
        if not self.enabled:
            return url_encode(MultiDict(args))
        else:
            if self.mode == Mode.MITIGATE:
                """Mitigate the xss by escaping"""
                return self.__get_escaped_args(args)
            elif self.mode == Mode.BLOCK:
                """Block the thingy and return error pages"""
                if self.__get_escaped_args(args) != url_encode(args):
                    """Something was changed"""
                    raise XSSException("XSS attempt detected.")
            else:
                """Return some error"""
                raise XSSException("Invalid mode for XSS module.")

    @staticmethod
    def __get_escaped_args(args):
        arguments = []
        for arg in args:
            arguments.append((arg, escape(args[arg])))
        arguments = url_encode(MultiDict(arguments))
        return arguments

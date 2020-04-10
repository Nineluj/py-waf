from flask import escape
from werkzeug.datastructures import MultiDict
from werkzeug.urls import url_encode

from waf.exceptions.xss_exception import XSSException
from waf.custom_types.module_mode import Mode
from waf.custom_types.request_type import RequestType

"""
XSS Checks
"""


class XSSCheck(object):
    def __init__(self, app):
        self.app = app
        self.enabled = (app.config['modules'].get('xss', {'enabled': True})).get('enabled', True)
        self.mode = Mode((app.config['modules'].get('xss', {'mode': Mode.MITIGATE})).get('mode', Mode.MITIGATE))
        supported_modes = {Mode.MITIGATE, Mode.BLOCK}
        if self.mode not in supported_modes:
            self.mode = Mode.MITIGATE

    def __call__(self, args: MultiDict, request_type=RequestType.DEFAULT):
        if not self.enabled:
            if request_type == RequestType.GET:
                return url_encode(MultiDict(args))
            else:
                return MultiDict(args)
        else:
            if self.mode == Mode.MITIGATE:
                """Mitigate the xss by escaping"""
                if request_type == RequestType.GET:
                    return url_encode(self.__get_escaped_args(args))
                else:
                    return self.__get_escaped_args(args)
            elif self.mode == Mode.BLOCK:
                """Block the thingy and return error pages"""
                if self.__get_escaped_args(args) != args:
                    """Something was changed"""
                    raise XSSException("XSS attempt detected.")
                else:
                    if request_type == RequestType.GET:
                        return url_encode(args)
                    else:
                        return args
            else:
                """Return some error"""
                raise XSSException("Invalid mode for XSS module.")

    @staticmethod
    def __get_escaped_args(args):
        arguments = []
        for arg in args:
            arguments.append((arg, escape(args[arg])))
        return MultiDict(arguments)

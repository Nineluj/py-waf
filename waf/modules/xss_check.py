from flask import escape
from werkzeug.datastructures import MultiDict
from werkzeug.urls import url_encode

"""
XSS Checks
"""


class XSSCheck(object):
    def __init__(self, app):
        self.app = app
        self.enabled = app.config['modules'].pop('xss', True)

    def __call__(self, query_string: MultiDict):
        if not self.enabled:
            return url_encode(MultiDict(query_string))
        else:
            qs = []
            for arg in query_string:
                qs.append((arg, escape(query_string[arg])))
            qs = url_encode(MultiDict(qs))
            return qs

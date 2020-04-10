import re

from werkzeug.datastructures import MultiDict
from werkzeug.urls import url_decode, url_encode

from waf.modules.xss import Mode
from waf.exceptions.sqli_exception import SQLIException
from waf.types.module_mode import Mode

INVALID_INPUT = [
    "--", "[^a-z,A-Z,0-9]\'[^a-z,A-Z,0-9]", "\"", r" \* ", "=", r"/",
    "\\\\", ";", "`", "^,", r"\|\|", "^\'", "[^s]*\' ",
    "%[0-9][0-9]",
    "DROP ", "SELECT ", r"AND .", r"ORDER BY .*",
    r"[0-9]-(true|false)", r"%[0-9][0-9]", r"(sleep|SLEEP)\(.*\)", r"benchmark\(.*\)", r"@@variable", "waitfor delay \'"
]


class SQLCheck(object):
    def __init__(self, app):
        self.enabled = (app.config['modules'].get('sqli', {'enabled': True})).get('enabled', True)
        self.mode = Mode((app.config['modules'].get('sqli', {'mode': 0})).get('mode', 0))
        supported_modes = {Mode.BLOCK, Mode.MITIGATE}
        if self.mode not in supported_modes:
            self.mode = Mode.BLOCK

    def __call__(self, content, method):
        if method == 'POST':
            if self.enabled:
                for key in content:
                    if not sql_injection_check(content[key], []):
                        raise SQLIException
        elif method == 'GET':
            if not content:
                return content
            arguments = []
            if self.enabled:
                decoded = url_decode(content)
                print("DICTIONARY INPUT:", decoded)
                for key in decoded:
                    if not sql_injection_check(decoded[key], []):
                        if self.mode == Mode.BLOCK:
                            raise SQLIException
                        elif self.mode == Mode.MITIGATE:
                            arguments.append((key, ""))
                    else:
                        arguments.append((key, decoded[key]))
            return url_encode(MultiDict(arguments))


def sql_injection_check(content, allowed=None) -> bool:
    if allowed is None:
        allowed = []
    for invalid in [item for item in INVALID_INPUT if item not in allowed]:
        # Deem any input that is unable to be REGEXED to be malicious in some way
        try:
            if re.search(invalid, content):
                return False
        except:
            return False
    return True

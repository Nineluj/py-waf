import re

INVALID_INPUT = [
    "--", "\'", "\"", "\*", "=", r"/", "\\\\", ";", "`", "^,"
    "DROP ", "SELECT ", r"AND .", r"ORDER BY .*",
    r"[0-9]-(true|false)", r"%[0-9][0-9]", r"(sleep|SLEEP)\(.*\)", r"benchmark\(.*\)", r"@@variable"
]


def sql_injection_check(content, allowed=None) -> bool:
    if allowed is None:
        allowed = []
    for invalid in [item for item in INVALID_INPUT if item not in allowed]:
        if re.search(invalid, content):
            return False
    return True

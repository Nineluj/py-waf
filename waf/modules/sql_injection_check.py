import re

INVALID_INPUT = [
    "--", "\'", "\""
]


def sql_injection_check(content, allowed=[]) -> bool:
    for invalid in [item for item in INVALID_INPUT if item not in allowed]:
        if re.search(invalid, content):
            return False
    return True

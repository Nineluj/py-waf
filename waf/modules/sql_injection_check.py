import re

INVALID_INPUT = [
    "--", "\'", "\"", "\*", "=", " /", ";",
    "DROP ", "SELECT "
]


def sql_injection_check(content, allowed=None) -> bool:
    if allowed is None:
        allowed = []
    for invalid in [item for item in INVALID_INPUT if item not in allowed]:
        print("\n\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n\n")
        print("Content:", content)
        if re.search(invalid, content):
            return False
    return True

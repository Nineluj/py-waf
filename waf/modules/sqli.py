import re

INVALID_INPUT = [
    "--", "[^a-z,A-Z,0-9]\'[^a-z,A-Z,0-9]", "\"", "\*", "=", r"/", "\\\\", ";", "`", "^,", r"\|\|", "^\'", "[^s]*\' ",
    "\+", "%[0-9][0-9]"
    "DROP ", "SELECT ", r"AND .", r"ORDER BY .*",
    r"[0-9]-(true|false)", r"%[0-9][0-9]", r"(sleep|SLEEP)\(.*\)", r"benchmark\(.*\)", r"@@variable", "waitfor delay \'"
]


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

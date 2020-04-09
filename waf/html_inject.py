from flask import render_template

BODY_TAG = "<body"


def inject_warning(page: bytes):
    # TODO: load the stylesheet separately into the head of the document
    warn = render_template("/warning.html", info="Warning will be displayed here!")
    return inject(page.decode(encoding='UTF-8'), warn).encode(encoding='UTF-8')


def inject(original: str, new_div: str) -> str:
    try:
        body_end = original.index(BODY_TAG) + len(BODY_TAG)

        inject_location = body_end
        while inject_location < len(original):
            if original[inject_location] == ">":
                break
            if original[inject_location] == "<":
                # we failed, somehow missed body tag close
                return ""
            inject_location += 1

        result = original[:inject_location + 1] + new_div + original[inject_location + 1:]
        return result
    except ValueError as ve:
        # we failed here as well
        # TODO: log failure
        return original

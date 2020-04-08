from flask import request, Blueprint, current_app as app, redirect, url_for
from requests import get
from requests.models import Response


REDIRECT_CODES = {301, 302, 303, 305, 307}
EXCLUDED_HEADERS = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
reverse_proxy = Blueprint('reverse_proxy', __name__)
print("reverse proxy defined")


# TODO: Add more interesting error message
def make_500() -> Response:
    r = Response()
    r.status_code = 500
    return r


# Simple function for proxying the request to the server
@reverse_proxy.route('/<path:path>', methods=['GET', 'POST'])
def proxy(path):
    if 'server_addr' not in app.config:
        return make_500()

    server_addr = app.config['server_addr']

    if request.method == 'GET':
        resp = get(url=f'http://{server_addr}/{path}')
        headers = [(name, value) for (name, value) in resp.raw.headers.items()
                   if name.lower() not in EXCLUDED_HEADERS]

        # TODO handle redirects properly
        if resp.status_code in REDIRECT_CODES:

            return redirect(url_for("index.php"), resp.status_code, resp.content)

        # Flask routes can accept tuple (content, status, headers)
        return resp.content, resp.status_code, headers
    else:
        # TODO: Implement other methods
        return make_500()


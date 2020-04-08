from flask import request, Blueprint, current_app as app, redirect, url_for
from requests import get
from urllib.parse import urlparse

REDIRECT_CODES = {301, 302, 303, 305, 307}
EXCLUDED_HEADERS = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
reverse_proxy = Blueprint('reverse_proxy', __name__)


# TODO: Add more interesting error message
def make_400():
    return "Record not found", 400


# Simple function for proxying the request to the server
@reverse_proxy.route('/', defaults={'path': ''})
@reverse_proxy.route('/<path:path>', methods=['GET', 'POST'])
def proxy(path):
    if 'server_addr' not in app.config:
        return make_400()

    server_addr = app.config['server_addr']

    if request.method == 'GET':
        print(f'http://{server_addr}/{path}')
        resp = get(url=f'http://{server_addr}/{path}', allow_redirects=False)
        headers = [(name, value) for (name, value) in resp.raw.headers.items()
                   if name.lower() not in EXCLUDED_HEADERS]

        # TODO handle redirects properly
        if resp.status_code in REDIRECT_CODES:
            o = urlparse(resp.raw.headers['Location'])

            if o.query:
                new_resource_path = f"{o.path}?{o.query}"
            else:
                new_resource_path = o.path

            return redirect(new_resource_path, code=resp.status_code)

        # Flask routes can accept tuple (content, status, headers)
        return resp.content, resp.status_code, headers
    else:
        # TODO: Implement other methods
        return make_400()


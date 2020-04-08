from src.main import app
from flask import request
from requests import get
from requests.models import Response


EXCLUDED_HEADERS = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']


# TODO: Add more interesting error message
def make_500():
    r = Response()
    r.status_code = 500
    return r


# Simple function for proxying the request to the server
@app.route('/<path:path>', methods=['GET', 'POST'])
def proxy(path):
    if 'server_addr' not in app.config:
        return make_500()

    server_addr = app.config['server_addr']

    if request.method == 'GET':
        resp = get(f'{server_addr}{path}')
        headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in EXCLUDED_HEADERS]

        proxied_response = Response()
        proxied_response.content(resp.content)
        proxied_response.status_code = resp.status_code
        proxied_response.headers = headers

        return proxied_response
    else:
        # TODO: Implement other methods
        return make_500()


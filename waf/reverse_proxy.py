from flask import request, Blueprint, current_app as app, redirect
import requests
from urllib.parse import urlparse

EXCLUDED_HEADERS = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
reverse_proxy = Blueprint('reverse_proxy', __name__)


def make_400():
    """Return a generic 404 error that flask can understand"""
    return "Record not found", 400


def get_app_url(path):
    """Resolve requested path into the address on the application server"""
    server_addr = app.config['server_addr']
    rest = ""

    if request.query_string:
        qs = request.query_string.decode()
        rest = f"?{qs}"

    return f"http://{server_addr}/{path}{rest}"


def get_filtered_headers(resp: requests.Response):
    """Gets the headers that don't include data specific for the proxied request from the Response"""
    return [(name, value) for (name, value) in resp.raw.headers.items()
            if name.lower() not in EXCLUDED_HEADERS]


# Simple function for proxying the request to the server
@reverse_proxy.route('/', defaults={'path': ''})
@reverse_proxy.route('/<path:path>', methods=['GET', 'POST'])
def proxy(path):
    if 'server_addr' not in app.config:
        return make_400()

    app_url = get_app_url(path)

    if request.method == 'GET':
        resp = requests.get(url=app_url, allow_redirects=False)
        headers = get_filtered_headers(resp)

        # We need to handle redirects correctly
        if resp.is_redirect:
            o = urlparse(resp.raw.headers['Location'])
            # We need to append "?" before query param
            new_resource_path = f"{o.path}?{o.query}" if o.query else o.path

            return redirect(new_resource_path, code=resp.status_code)

        # Flask routes can accept tuple (content, status, headers)
        return resp.content, resp.status_code, headers
    elif request.method == "POST":
        resp = requests.post(url=app_url, data=request.get_data())

        return resp.content, resp.status_code, get_filtered_headers(resp)
    else:
        # TODO: Implement other methods
        return make_400()

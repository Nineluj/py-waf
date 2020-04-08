from flask import request, Blueprint, current_app as app, redirect
import requests
from urllib.parse import urlparse
from typing import List, Dict, Tuple

EXCLUDED_HEADERS = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
reverse_proxy = Blueprint('reverse_proxy', __name__)


def make_400():
    """Return a generic 404 error that flask can understand"""
    return "Record not found", 400


def get_app_url(path: str) -> str:
    """Resolve requested path into the address on the application server"""
    server_addr = app.config['server_addr']
    rest = ""

    if request.query_string:
        qs = request.query_string.decode()
        rest = f"?{qs}"

    return f"http://{server_addr}/{path}{rest}"


def filter_headers_app_request(headers) -> Dict[str, str]:
    """Gets the headers from the client request that can be passed on to the application server"""
    new_headers = {}

    for name, value in headers.items():
        if name.lower() not in EXCLUDED_HEADERS:
            new_headers[name] = value

    return new_headers


def get_filtered_headers_client_response(resp: requests.Response) -> List[Tuple[str, str]]:
    """Gets the headers that don't include data specific for the proxied request from the Response"""
    headers = resp.raw.headers
    return [(name, value) for (name, value) in headers.items()
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
        headers = get_filtered_headers_client_response(resp)

        # We need to handle redirects correctly
        if resp.is_redirect:
            o = urlparse(resp.raw.headers['Location'])
            # We need to append "?" before query param
            new_resource_path = f"{o.path}?{o.query}" if o.query else o.path

            return redirect(new_resource_path, code=resp.status_code)

        # Flask routes can accept tuple (content, status, headers)
        return resp.content, resp.status_code, headers
    elif request.method == "POST":
        app_request_headers = filter_headers_app_request(dict(request.headers))
        resp = requests.post(url=app_url, data=request.get_data(), headers=app_request_headers)
        return resp.content, resp.status_code, get_filtered_headers_client_response(resp)
    else:
        # TODO: Implement other methods
        return make_400()

from typing import List, Dict, Tuple
from urllib.parse import urlparse

import requests
from flask import request, Blueprint, current_app as app, redirect

from waf.exceptions.credential_exception import CredentialException
from waf.exceptions.xss_exception import XSSException
from waf.exceptions.sqli_exception import SQLIException
from waf.modules.credential import CredentialCheck
from waf.modules.xss import XSSCheck, RequestType
from waf.modules.sqli import SQLCheck

from waf.helper import make_error_page
from waf.html_inject import inject_warning

EXCLUDED_HEADERS = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
reverse_proxy = Blueprint('reverse_proxy', __name__)


def get_app_url(path: str) -> str:
    """Resolve requested path into the address on the application server"""
    server_addr = app.config['server_addr']
    rest = ""

    if request.query_string:
        """Parse and escape any query parameters"""
        qs = XSSCheck(app)(request.args, RequestType.GET)
        rest = f"?{qs}"

    if "http://" in server_addr:
        return f"{server_addr}/{path}{rest}"
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
        return make_error_page(500, "Server address hasn't been configured", unexpected=True)

    # This is for demonstration purposed, don't remove
    if path == "throwerror":
        return make_error_page(500, "Intentionally throwing error", unexpected=True)

    try:
        app_url = get_app_url(path)
    except XSSException as ex:
        return make_error_page(666, str(ex))

    timeout = get_timeout()

    if request.method == 'GET':
        return handle_get(app_url, timeout)
    elif request.method == "POST":
        return handle_post(app_url, timeout)
    else:
        # TODO: Implement other methods
        return make_error_page(500, f"Method ({request.method}) has not been implemented", unexpected=True)


def get_timeout() -> int:
    if 'timeout' in app.config:
        return app.config['timeout']
    else:
        return 5


def handle_get(app_url, timeout):
    app_request_headers = filter_headers_app_request(dict(request.headers))
    app.logger.info(f"Retrieving URL: {app_url}")

    try:
        resp = requests.get(url=app_url,
                            allow_redirects=False,
                            headers=app_request_headers,
                            timeout=timeout)
    except requests.exceptions.Timeout:
        return make_error_page(504, "Connection to application timed out", unexpected=True)
    except requests.exceptions.ConnectionError:
        return make_error_page(504, "Unable to connect to the application server", unexpected=True)

    headers = get_filtered_headers_client_response(resp)

    # We need to handle redirects correctly
    if resp.is_redirect:
        o = urlparse(resp.raw.headers['Location'])
        # We need to append "?" before query param
        new_resource_path = f"{o.path}?{o.query}" if o.query else o.path

        return redirect(new_resource_path, code=resp.status_code)

    content = resp.content

    # Flask routes can accept tuple (content, status, headers)
    return content, resp.status_code, headers


def handle_post(app_url, timeout):
    app_request_headers = filter_headers_app_request(dict(request.headers))
    data = request.form

    # Need to check form AFTER the request.get_data() call, or else the form will be missing from that data
    try:
        is_credential_page = CredentialCheck(app)(request.path, request.form)
    except CredentialException as ex:
        # TODO may want to issue a warning instead
        if isinstance(data, (bytes, bytearray)) \
                and "Content-Type" in app_request_headers \
                and "text/html" in app_request_headers['Content-Type']:
            content = inject_warning(data)
        return make_error_page(403, str(ex))

    if not is_credential_page:
        try:
            SQLCheck(app)(request.form)
        except SQLIException:
            return make_error_page(403, "Failed SQL form verification")

        try:
            """Check for xss in fields"""
            data = XSSCheck(app)(request.form, RequestType.POST)
        except XSSException as ex:
            return make_error_page(666, str(ex))

    app.logger.info(f"Making POST: {app_url}")
    try:
        resp = requests.post(url=app_url,
                             data=data,
                             headers=app_request_headers,
                             allow_redirects=False,
                             timeout=timeout)
    except requests.exceptions.Timeout:
        return make_error_page(504, "Connection to application timed out", unexpected=True)
    except requests.exceptions.ConnectionError:
        return make_error_page(504, "Unable to connect to the application server", unexpected=True)

    if resp.is_redirect:
        o = urlparse(resp.raw.headers['Location'])
        # We need to append "?" before query param
        new_resource_path = f"{o.path}?{o.query}" if o.query else o.path

        return redirect(new_resource_path, code=resp.status_code)

    return resp.content, resp.status_code, get_filtered_headers_client_response(resp)

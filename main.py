from flask import escape
import functions_framework

from controller.sites_bulk_load import sites_bulk_load


@functions_framework.http
def hello_http(request):
    body = request.get_json(silent=True)
    request_args = request.args
    method = request.method
    headers = request.headers

    try:
        if method == 'POST':
            # sites_bulk_load(body,headers["Authorization"])
            return ('', 200, None)
    except:
        return ('Fallamos', 500, None)

from flask import escape
import functions_framework

from controller.sites_bulk_load import sites_bulk_load


@functions_framework.http
def hello_http(request):
    body = request.get_json(silent=True)
    request_args = request.args
    method = request.method
    headers = request.headers
    if body and 'quoteId' in body and 'accountId' in body and 'sites' in body:

        try:
            if method == 'POST':
                # sites_bulk_load(body,headers["Authorization"])
                return ('', 200, None)
        except:
            return ('Internal Server Error', 500, None)

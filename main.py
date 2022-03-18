from flask import escape
import functions_framework

from controller.sites_bulk_load import sites_bulk_load

@functions_framework.http
def hello_http(request):
    body = request.get_json(silent=True)
    request_args = request.args
    method = request.method

    if method == 'POST':
        sites_bulk_load(body)

    if body and 'name' in body:
        name = body['name']
    elif request_args and 'name' in request_args:
        name = request_args['name']
    else:
        name = 'World'
    return f'Hello {escape(name)}!'

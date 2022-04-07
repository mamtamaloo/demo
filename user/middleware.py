from flask_principal import PermissionDenied
from werkzeug import Request


class Middleware:
    def __init__(self,app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        self._handle_request(request)
        return self.app(environ, start_response)

    def _handle_request(self, request):
        client_id = "mamta"
        client_secret = "maloo"
        if not (client_id == request.headers['x-client-id'] and client_secret == request.headers['x-client-secret']):
            raise PermissionDenied
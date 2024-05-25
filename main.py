from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from endpoints.authorize import checkAndSendAuthorizeUI
from util.http import returnErrorUIToUA

HTTP_PORT=8080
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/authorize'):
            checkAndSendAuthorizeUI(self)
        else:
            returnErrorUIToUA(self,"invalid_page", "The authorization server does not support obtaining an authorization code using this method."
        )
    # authorizationにおいてはPOSTのサポートは義務ではない。(May)
    def do_POST(self):
       match(self.path):
            case '/authorize':
                checkAndSendAuthorizeUI(self)
            case _:
                returnErrorUIToUA(self, "invalid_page", "The authorization server does not support obtaining an authorization code using this method."
        )
def run(server_class, handler_class, port):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run(HTTPServer,RequestHandler,HTTP_PORT)
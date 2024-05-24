from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from endpoints.authorize import authorizeUI
from util.http import sendSimpleResponse

HTTP_PORT=8080
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/authorize'):
            authorizeUI(self)
        else:
            sendSimpleResponse(self,404,json.dumps({
            "error": "invalid_page",
            "error_description": "The authorization server does not support obtaining an authorization code using this method."
        }))
    def do_POST(self):
       match(self.path):
            case '/authorize':
                authorizeUI(self)
            case _:
                sendSimpleResponse(self,404,json.dumps({
            "error": "invalid_page",
            "error_description": "The authorization server does not support obtaining an authorization code using this method."
        }))
def run(server_class, handler_class, port):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run(HTTPServer,RequestHandler,HTTP_PORT)
from http.server import BaseHTTPRequestHandler, HTTPServer
from endpoints.authorize import authorizeUI
from util.http import sendSimpleResponse

HTTP_PORT=80
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        match(self.path):
            case '/authorize':
                authorizeUI(self)
            case _:
                sendSimpleResponse(self,404,"invalid page")
def run(server_class, handler_class, port):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run(HTTPServer,RequestHandler,80)
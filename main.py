from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from endpoints.authorize import checkAndAuthorizeAndSend, checkAndSendAuthorizeUI, checkAndSendToken
from util.http import returnErrorUIToUA

HTTP_PORT=8080
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/authorize'):
            checkAndSendAuthorizeUI(self)
        elif self.path.startswith('/loginAndAuthorize'):
            returnErrorUIToUA(self,"invalid_method", "Send credencial information with post.")
        elif self.path.startswith("/access_token"):
            checkAndSendToken(self)
        else:
            returnErrorUIToUA(self,"invalid_page", "The authorization server does not support obtaining an authorization code using this method.")
    def do_POST(self):
        # 一応サポートしてるけど、Postのサポートは義務ではない
        if self.path.startswith('/authorize'):
                checkAndSendAuthorizeUI(self)
        elif self.path.startswith('/loginAndAuthorize'):
                checkAndAuthorizeAndSend(self)
        else:
                returnErrorUIToUA(self, "invalid_page", "The authorization server does not support obtaining an authorization code using this method.")
def run(server_class, handler_class, port):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run(HTTPServer,RequestHandler,HTTP_PORT)
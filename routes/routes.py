from http.server import BaseHTTPRequestHandler
from routes.authorize_code_flow.authorization import checkAndAuthorizeAndSend, checkAndSendAuthorizeUI, checkAndSendToken
from util.assembleResponse import returnErrorUIToUA
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
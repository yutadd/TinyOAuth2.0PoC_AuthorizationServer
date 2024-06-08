from http.server import BaseHTTPRequestHandler
from routes.authorize_code_flow.authentication import SendAuthenticateUI, check_loggedIn_and_redirect, processLoginAndRedirectToAuthorize
from routes.authorize_code_flow.authorization import SendAuthorizationUI, checkAndAuthorizeAndSendCode
from util.assembleResponse import returnErrorUIToUA
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path=self.path.split('?')[0].split('#')[0]
        if path=='/authorize/check_loggedin':
            check_loggedIn_and_redirect(self)
        elif path=='/authorize/ask/login':
            SendAuthenticateUI(self)
        elif path=='/authorize/ask/authorize':
            SendAuthorizationUI(self)
        elif  path=='/authorize/act/authorize':
            checkAndAuthorizeAndSendCode(self)
        else:
            returnErrorUIToUA(self,"invalid_page", "this path is not on routes.")
    def do_POST(self):
        path=self.path.split('?')[0].split('#')[0]
        if path=="/authorize/act/login":
            processLoginAndRedirectToAuthorize(self)
        elif self.path.startswith('/act/exchangeToken'):
            pass
from http.server import BaseHTTPRequestHandler
from routes.authorize_code_flow.authentication import SendAuthenticateUI, check_loggedIn_and_redirect, processLoginAndRedirectToAuthorize
from routes.authorize_code_flow.authorization import SendAuthorizationUI, checkAndAuthorizeAndSendCode, checkAndSendToken
from util.assembleResponse import returnErrorUIToUA
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/authorize/check_loggedin'):
            check_loggedIn_and_redirect(self)
        elif self.path.startswith('/authorize/ask/login'):
            SendAuthenticateUI(self)
        elif self.path.startswith('/authorize/ask/login'):
            SendAuthorizationUI(self)
        elif  self.path.startswith('/authorize/act/authorize'):
            checkAndAuthorizeAndSendCode(self)
        else:
            returnErrorUIToUA(self,"invalid_page", "this path is not on routes.")
    def do_POST(self):
        if self.path.startswith("/authorize/act/login"):
            processLoginAndRedirectToAuthorize(self)
        # TODO: TokenエンドポイントはPOSTを推奨している(?)
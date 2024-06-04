from http.server import BaseHTTPRequestHandler
from routes.authorize_code_flow.authentication import check_loggedIn_and_redirect, processLoginAndRedirectToAuthorize
from routes.authorize_code_flow.authorization import checkAndSendToken
from util.assembleResponse import returnErrorUIToUA
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/authorize/check_loggedin'):
            check_loggedIn_and_redirect(self)
        elif self.path.startswith('/authorize/ask'):
            pass
        else:
            returnErrorUIToUA(self,"invalid_page", "this path is not on routes.")
    def do_POST(self):
        if self.path.startswith("/authorize/login"):
            processLoginAndRedirectToAuthorize(self)
        # TODO: TokenエンドポイントはPOSTを推奨している(?)
        
        pass
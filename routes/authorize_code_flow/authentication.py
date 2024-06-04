# UI & login api
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from util.CheckRequest import checkAuthorizationRequest
from util.db.client import getClientById
from util.assembleResponse import return_sessionId_and_redirect, returnErrorUIToUA, returnAuthenticateUIToUA, sendRedirectAndCodeToClient
from util.db.user import do_login
from util.db.user import check_loggedin_by_sessionid

def SendAuthenticateUI(context: BaseHTTPRequestHandler):
    query_components = parse_qs(urlparse(context.path).query)
    client_id=query_components.get('client_id', [None])[0]
    success_redirect_uri = query_components.get(
        'success_redirect_uri', [None])[0]
    fail_redirect_uri = query_components.get('fail_redirect_uri', [None])[0]
    requested_scope = query_components.get('scope', [None])[0]
    state = query_components.get('state', [None])[0]
    response_type = query_components.get('response_type', [None])[0]
    returnAuthenticateUIToUA(context=context,client_id=client_id,fail_redirect_uri=fail_redirect_uri,response_type=response_type,scope=requested_scope,state=state,success_redirect_uri=success_redirect_uri)

def check_loggedIn_and_redirect(context: BaseHTTPRequestHandler):
    query_components = parse_qs(urlparse(context.path).query)
    session_id = query_components.get('session_id', [None])[0]
    query_string = context.path.split('?', 1)[1] if '?' in context.path else ''
    if session_id and check_loggedin_by_sessionid(session_id):
        context.send_response(302)
        context.send_header('Location', f"http://localhost:8080/authorize/ask/authorize?{query_string}")
        context.end_headers()
    else:
        context.send_response(302)
        context.send_header('Location', f"http://localhost:8080/authorize/ask/login?{query_string}")
        context.end_headers()
        
def processLoginAndRedirectToAuthorize(context: BaseHTTPRequestHandler):
    content_length = int(context.headers['Content-Length'])
    post_data = context.rfile.read(content_length)
    query_components = parse_qs(post_data.decode('utf-8'))
    username = query_components.get('username', [None])[0]
    password = query_components.get('password', [None])[0]
    session_id=do_login(username, password)
    if session_id is not None:
        returnErrorUIToUA(context, "access_denied",
                            "Invalid username or password.")
    else:
        return_sessionId_and_redirect(context,session_id)

# クライアント認証はトークンエンドポイントでのみ行う
#   # if auth_header:
    #     auth_type, auth_info = auth_header.split(' ', 1)
    #     if auth_type.lower() == 'basic':
    #         decoded_auth_info = base64.b64decode(auth_info).decode('utf-8')
    #         client_id, password = decoded_auth_info.split(':', 1)
    #         print(f"Username: {client_id}, Password: {password}")
    #         if authenticate_client(client_id, password):
    #             if checkAuthorizationRequest(context=context, success_redirect_uri=success_redirect_uri, client_provided_state=client_provided_state, fail_redirect_uri=fail_redirect_uri, registeredClient=registeredClient, requested_scope=requested_scope, response_type=response_type, response_type=response_type):
    #                 returnAuthorizationUIToUA(context=context, scope=requested_scope, fail_redirect_uri=fail_redirect_uri,
    #                                   client_id=registeredClient.client_id, success_redirect_uri=success_redirect_uri, response_type=response_type, state=state)
    #             else:
    #                 returnErrorUIToUA(
    #                     context, "invalid_params", "there are any params we don't recognize in your request.")
    #         else:
    #             returnErrorUIToUA(context, "invalid_client",
    #                               "Client_id you provided is not recognized.")
    #     else:
    #         returnErrorUIToUA(context, "invalid_authentication_method",
    #                           "We support only basic authentication method")
    # else:
    #     returnErrorUIToUA(context, "invalid_authentication_header",
    #                       "we support only confidential client.")
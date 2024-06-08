import datetime
from http.server import BaseHTTPRequestHandler
from typing import List
from util.db.client import SearchClientByAnyColumn

import bcrypt

from util.assembleResponse import returnErrorUIToUA, sendRedirectAndErrorToClient
from util.db.user import check_loggedin_by_sessionid, is_code_valid


def checkAuthorizationRequest(context: BaseHTTPRequestHandler, response_type:str,registeredClient,success_redirect_uri,fail_redirect_uri,requested_scope,client_provided_state,session_id:str) -> bool:
    if requested_scope is None or not set(requested_scope.split()).issubset(set(registeredClient.allowed_scope)):
        sendRedirectAndErrorToClient(
            context, "invalid_scope", "The requested scope is invalid, unknown, or malformed.", redirect_uri=fail_redirect_uri, state=client_provided_state)
        return False
    return True

'''
アクセストークンリクエスト
 POST /token HTTP/1.1
    Host: server.example.com
    Content-Type: application/x-www-form-urlencoded

    grant_type=authorization_code&code=SplxlOBeZQQYbYS6WxSbIA&success_redirect_uri=http://localhost/access_token_success&fail_redirect_uri=http://localhost/access_token_fail
コンフィデンシャルクライアント以外はclient_idも必須
'''
def checkAccessTokentRequest(context: BaseHTTPRequestHandler, success_redirect_uri:str,registeredClient,fail_redirect_uri,client_provided_code,client_provided_grant_type) -> bool:
    if success_redirect_uri is None or not success_redirect_uri.startswith(registeredClient.redirect_prefix):
        returnErrorUIToUA(context=context, error="invalid_request",
            error_detail="The success_redirect_uri is invalid.")
        return False
    if fail_redirect_uri is None or not fail_redirect_uri.startswith(registeredClient.redirect_prefix):
        returnErrorUIToUA(context=context, error="invalid_request",
            error_detail="The success_redirect_uri is invalid.")
        return False
    if client_provided_grant_type != "authorization_code":
        returnErrorUIToUA(context, error="invalid grant_type",
            error_detail="We support only authorization_code")
        return False
    user = is_code_valid(client_provided_code)

def isloggedIn(context: BaseHTTPRequestHandler) -> bool:
    session_id = context.headers.get('Cookie', '').split('session_id=')[-1].split(';')[0]
    if session_id and check_loggedin_by_sessionid(session_id):
        return True
    else:
        return False
    
def check_redirect_urls(urls:List[str],client_id:str)->bool:
    clients=SearchClientByAnyColumn('client_id',client_id)
    if len(clients)>0:
        client=clients[0]
        for url in urls:
            if not url.startswith(client.redirect_prefix):
                return False
        return True
    else:
        return False
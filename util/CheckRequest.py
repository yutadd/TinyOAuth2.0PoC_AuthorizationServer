import datetime
from http.server import BaseHTTPRequestHandler

from util.assembleResponse import returnErrorUIToUA, sendRedirectAndErrorToClient
from util.db.user import getUserByCode


def checkAuthorizationRequest(context: BaseHTTPRequestHandler, response_type:str,registeredClient,success_redirect_uri,fail_redirect_uri,requested_scope,client_provided_state) -> bool:
    if registeredClient is None:
        returnErrorUIToUA(context, "invalid_client_id",
                          "The client is not authorized to request an authorization code using this method.")
        return
    print("CAR success_redirect_uri:",success_redirect_uri)
    if success_redirect_uri is None or not success_redirect_uri.startswith(registeredClient.redirect_prefix):
        returnErrorUIToUA(context=context, error="invalid_request",
                          error_detail="The success_redirect_uri is invalid.")
        return False
    if fail_redirect_uri is None or not fail_redirect_uri.startswith(registeredClient.redirect_prefix):
        returnErrorUIToUA(context=context, error="invalid_request",
                          error_detail="The fail_redirect_uri is invalid.")
        return False
    if response_type != 'code':
        sendRedirectAndErrorToClient(context, "unsupported_response_type",
                                     "The authorization server does not support obtaining an authorization code using this method.", fail_redirect_uri, client_provided_state)
        return False
    if requested_scope is None or not set(requested_scope.split()).issubset(set(registeredClient.allowed_scope.split(' '))):
        sendRedirectAndErrorToClient(
            context, "invalid_scope", "The requested scope is invalid, unknown, or malformed.", redirect_uri=fail_redirect_uri, state=client_provided_state)
        return False
    return True

'''
アクセストークンリクエスト
 POST /token HTTP/1.1
     Host: server.example.com
     Content-Type: application/x-www-form-urlencoded

     grant_type=authorization_code&code=SplxlOBeZQQYbYS6WxSbIA
     &success_redirect_uri=http://localhost/access_token_success&fail_redirect_uri=http://localhost/access_token_fail
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
    user = getUserByCode(client_provided_code)
    # Authorization Codeが発行されてから5分以内かどうかを確認
    if user and (datetime.datetime.now() - user.authorization_code_issued_at).total_seconds() <= 300 and user[1] == client_provided_code:
        return True
    else:
        return False

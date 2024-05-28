import datetime
from http.server import BaseHTTPRequestHandler

from util.http import returnErrorUIToUA, sendRedirectAndErrorToClient
from util.client import getClientById
from util.user import getUserByCode

'''
認可リクエスト
  GET /authorize?response_type=code&client_id=s6BhdRkqt3&state=xyz
        &success_redirect_uri=http://localhost/authorize_success&fail_redirect_uri=http://localhost/authorize_fail HTTP/1.1
    Host: server.example.com
'''
def checkAuthorizationRequest(context: BaseHTTPRequestHandler, query_components: dict[str, list[str]]) -> bool:
    registeredClient = getClientById(
        query_components.get('client_id', [None])[0])
    client_provided_state = query_components.get('state', [None])[0]
    if registeredClient is None:
        returnErrorUIToUA(context, "invalid_client_id",
                          "The client is not authorized to request an authorization code using this method.")
        return
    success_redirect_uri = query_components.get('success_redirect_uri', [None])[0]
    print("CAR success_redirect_uri:",success_redirect_uri)
    if success_redirect_uri is None or not success_redirect_uri.startswith(registeredClient.redirect_prefix):
        returnErrorUIToUA(context=context, error="invalid_request",
                          error_detail="The success_redirect_uri is invalid.")
        return False
    fail_redirect_uri = query_components.get('fail_redirect_uri', [None])[0]
    if fail_redirect_uri is None or not fail_redirect_uri.startswith(registeredClient.redirect_prefix):
        returnErrorUIToUA(context=context, error="invalid_request",
                          error_detail="The fail_redirect_uri is invalid.")
        return False
    if query_components.get('response_type', [None])[0] != 'code':
        sendRedirectAndErrorToClient(context, "unsupported_response_type",
                                     "The authorization server does not support obtaining an authorization code using this method.", fail_redirect_uri, client_provided_state)
        return False
    requested_scope = query_components.get('scope', [None])[0]
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


def checkAccessTokentRequest(context: BaseHTTPRequestHandler, query_components: dict[str, list[str]]) -> bool:
    client_provided_code = query_components.get('code', [None])[0]
    registeredClient = getClientById(
        query_components.get('client_id', [None])[0])
    success_redirect_uri = query_components.get('success_redirect_uri', [None])[0]
    client_provided_grant_type = query_components.get('grant_type', [None])[0]
    fail_redirect_uri = query_components.get('fail_redirect_uri', [None])[0]
    print("CATR code, client: ", client_provided_code)
    print("CATR success_redirect_uri client:", success_redirect_uri)
    print("CATR redirect_uri registered:", registeredClient.redirect_prefix)
    print(f"CATR allowed_scope client:", registeredClient.allowed_scope)
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

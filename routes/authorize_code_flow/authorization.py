

from http.server import BaseHTTPRequestHandler
from urllib import parse
from urllib.parse import urlparse, parse_qs

import bcrypt
from util.CheckRequest import checkAccessTokentRequest, checkAuthorizationRequest
from util.db.client import getClientById
from util.assembleResponse import returnErrorUIToUA, sendRedirectAndCodeToClient
from util.db.user import  getUserByUsername, issue_Access_Token

'''
TODO:ここですべての引数をクエリから取り出すようにする
'''
'''
認可リクエスト
  GET /authorize?response_type=code&client_id=s6BhdRkqt3&state=xyz
        &success_redirect_uri=http://localhost/authorize_success&fail_redirect_uri=http://localhost/authorize_fail HTTP/1.1
    Host: server.example.com
'''
def checkAndAuthorizeAndSendCode(context: BaseHTTPRequestHandler) -> bool:
    length = int(context.headers.get('content-length'))
    field_data = context.rfile.read(length)
    query_components = parse.parse_qs(str(field_data, "UTF-8"))
    registeredClient = getClientById(
    query_components.get('client_id', [None])[0])
    success_redirect_uri = query_components.get('success_redirect_uri', [None])[0]
    fail_redirect_uri = query_components.get('fail_redirect_uri', [None])[0]
    requested_scope = query_components.get('scope', [None])[0]
    client_provided_state = query_components.get('state', [None])[0]
    state = query_components.get('state', [None])[0]
    response_type=query_components.get('response_type', [None])[0]
    username=query_components.get('username', [''])[0]
    password=query_components.get('password', [''])[0]
    
    if not checkAuthorizationRequest(context=context, registeredClient=registeredClient,client_provided_state=client_provided_state,fail_redirect_uri=fail_redirect_uri,requested_scope=requested_scope,response_type=response_type,success_redirect_uri=success_redirect_uri):
        return False
  # 認証情報の検証


def checkAndSendToken(context: BaseHTTPRequestHandler):
    query_components = parse_qs(urlparse(context.path).query)
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
    if checkAccessTokentRequest(context=context,client_provided_code=client_provided_code,client_provided_grant_type=client_provided_grant_type,fail_redirect_uri=fail_redirect_uri,registeredClient=registeredClient,success_redirect_uri=success_redirect_uri ):
        issue_Access_Token(code=query_components.get('code', [''])[0])
        # TODO:発行したアクセストークンを送信する処理






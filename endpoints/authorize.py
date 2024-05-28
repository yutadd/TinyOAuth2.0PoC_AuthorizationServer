
import datetime
from http.server import BaseHTTPRequestHandler
from urllib import parse
from urllib.parse import urlparse, parse_qs

import bcrypt
from util.CheckRequest import checkAccessTokentRequest, checkAuthorizationRequest
from util.client import getClientById
from util.http import returnErrorUIToUA, returnLoginUIToUA, sendRedirectAndCodeToClient
from util.user import  getUserByUsername, issue_Access_Token

'''
TODO:ここですべての引数をクエリから取り出すようにする
'''
'''
認可リクエスト
  GET /authorize?response_type=code&client_id=s6BhdRkqt3&state=xyz
        &success_redirect_uri=http://localhost/authorize_success&fail_redirect_uri=http://localhost/authorize_fail HTTP/1.1
    Host: server.example.com
'''
def checkAndAuthorizeAndSend(context: BaseHTTPRequestHandler) -> bool:
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
    if not authenticate(username, password):
        returnErrorUIToUA(context, "access_denied",
                          "Invalid username or password.")
        return False
    sendRedirectAndCodeToClient(context=context, success_redirect_uri=success_redirect_uri,
                                state=state, username=username)

def checkAndSendAuthorizeUI(context: BaseHTTPRequestHandler):
    query_components = parse_qs(urlparse(context.path).query)
    if checkAuthorizationRequest(context, query_components):
        returnLoginUIToUA(context, query_components)


def checkAndSendToken(context: BaseHTTPRequestHandler):
    query_components = parse_qs(urlparse(context.path).query)
    if checkAccessTokentRequest(context, query_components):
        issue_Access_Token(code=query_components.get('code', [''])[0])


def authenticate(username: str, password: str):
    user = getUserByUsername(username)
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
        return True
    else:
        return False




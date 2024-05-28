
import datetime
from http.server import BaseHTTPRequestHandler
from urllib import parse
from urllib.parse import urlparse, parse_qs

import bcrypt
from util.CheckRequest import checkAccessTokentRequest, checkAuthorizationRequest
from util.http import returnErrorUIToUA, returnLoginUIToUA, sendRedirectAndCodeToClient
from util.user import  getUserByUsername, issue_Access_Token

'''
TODO:ここですべての引数をクエリから取り出すようにする
'''
def checkAndAuthorizeAndSend(context: BaseHTTPRequestHandler) -> bool:
    length = int(context.headers.get('content-length'))
    field_data = context.rfile.read(length)
    query_components = parse.parse_qs(str(field_data, "UTF-8"))
    state = query_components.get('state', [None])[0]
    if not checkAuthorizationRequest(context, query_components):
        return False
  # 認証情報の検証
    if not authenticate(query_components.get('username', [''])[0], query_components.get('password', [''])[0]):
        returnErrorUIToUA(context, "access_denied",
                          "Invalid username or password.")
        return False
    success_redirect_uri = query_components.get('success_redirect_uri', [None])[0]
    sendRedirectAndCodeToClient(context=context, success_redirect_uri=success_redirect_uri,
                                state=state, username=query_components.get('username', [''])[0])


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




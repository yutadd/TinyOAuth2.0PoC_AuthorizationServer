
import datetime
from http.server import BaseHTTPRequestHandler
from urllib import parse
from urllib.parse import urlparse, parse_qs

import bcrypt
from util.CheckRequest import checkAccessTokentRequest, checkAuthorizationRequest
from util.http import  returnErrorUIToUA, returnLoginUIToUA, sendRedirectAndCodeToClient
from util.user import authenticate, getUserByUsername, issue_Access_Token

def checkAndAuthorizeAndSend(context:BaseHTTPRequestHandler)->bool:
    length = int(context.headers.get('content-length'))
    field_data = context.rfile.read(length)
    query_components= parse.parse_qs(str(field_data,"UTF-8"))
    state=query_components.get('state', [None])[0]
    if not checkAuthorizationRequest(context,query_components):
        return False
  # 認証情報の検証
    if not authenticate(query_components.get('username', [''])[0], query_components.get('password', [''])[0]):
        returnErrorUIToUA(context, "access_denied", "Invalid username or password.")
        return False
    redirect_uri = query_components.get('redirect_uri', [None])[0]
    sendRedirectAndCodeToClient(context=context,redirect_uri=redirect_uri,state=state,username=query_components.get('username', [''])[0])
def checkAndSendAuthorizeUI(context:BaseHTTPRequestHandler):
    query_components = parse_qs(urlparse(context.path).query)
    if checkAuthorizationRequest(context,query_components):
        returnLoginUIToUA(context,query_components)
def checkAndSendToken(context:BaseHTTPRequestHandler):
    query_components = parse_qs(urlparse(context.path).query)
    if checkAccessTokentRequest(context,query_components):
        issue_Access_Token(code=query_components.get('code', [''])[0])
def authenticate(username:str,password:str):
    user=getUserByUsername(username)
    if user and bcrypt.checkpw(password.encode('utf-8'), user[0]):
        return True
    else:
        return False
def is_authorization_code_valid(username:str,code: str) -> bool:
    user=getUserByUsername(username)
    # Authorization Codeが発行されてから5分以内かどうかを確認
    if user and (datetime.datetime.now() - user.authorization_code_issued_at).total_seconds() <= 300 and user[1] == code:
        return True
    else:
        return False
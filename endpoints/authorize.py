
from http.server import BaseHTTPRequestHandler
from urllib import parse
from urllib.parse import urlparse, parse_qs
from util.http import  returnErrorUIToUA, returnLoginUIToUA, sendRedirectAndSuccessToClient
from util.request import checkParam
from util.user import authenticate

def checkAndAuthorizeAndSend(context:BaseHTTPRequestHandler)->bool:
    if context.headers.get('Content-Type') != 'application/x-www-form-urlencoded':
        returnErrorUIToUA(context, "invalid_request", "Content-Type must be application/x-www-form-urlencoded")
        return
    length = int(context.headers.get('content-length'))
    field_data = context.rfile.read(length)
    query_components= parse.parse_qs(str(field_data,"UTF-8"))
    state=query_components.get('state', [None])[0]
    if not checkParam(context,query_components):
        return False
  # 認証情報の検証
    if not authenticate(query_components.get('username', [''])[0], query_components.get('password', [''])[0]):
        returnErrorUIToUA(context, "access_denied", "Invalid username or password.")
        return False
    redirect_uri = query_components.get('redirect_uri', [None])[0]
    sendRedirectAndSuccessToClient(context=context,redirect_uri=redirect_uri,state=state)
'''
4.1.1を参考に
クライアントからのパラメータを解析し、認可するかどうか確認するUIを返す。
チェックするパラメータは以下の通り。
response_type,client_id,state,redirect_uri,scope
'''
def checkAndSendAuthorizeUI(context:BaseHTTPRequestHandler):
    if context.headers.get('Content-Type') != 'application/x-www-form-urlencoded':
        returnErrorUIToUA(context, "invalid_request", "Content-Type must be application/x-www-form-urlencoded")
        return
    query_components = parse_qs(urlparse(context.path).query)
    if checkParam(context,query_components):
        returnLoginUIToUA(context,query_components)
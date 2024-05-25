
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from util.http import  returnErrorUIToUA, returnLoginUIToUA
from util.request import checkParam

'''
contentは
application/x-www-form-urlencoded
'''
def checkAndAuthorizeAndSend(context:BaseHTTPRequestHandler):
    if context.headers.get('Content-Type') != 'application/x-www-form-urlencoded':
        returnErrorUIToUA(context, "invalid_request", "Content-Type must be application/x-www-form-urlencoded")
        return
    query_components = parse_qs(urlparse(context.path).query)
    checkParam(context,query_components)
    #if checkCredential(context):
        # sendsuccess
        #pass

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

from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from util.http import sendSimpleResponse

'''
contentは
application/x-www-form-urlencoded
'''
def authorize(context:BaseHTTPRequestHandler):
    pass

'''
4.1.1を参考に
クライアントからのパラメータを解析し、認可するかどうか確認するUIを返す。
チェックするパラメータは以下の通り。
response_type,client_id,state,redirect_uri,scope
'''
def authorizeUI(context:BaseHTTPRequestHandler):
    query_components = parse_qs(urlparse(context.path).query)
    if query_components.get('response_type', [None])[0]=='code':
        if query_components.get('client_id', [None])[0]=='1':
            if query_components.get('state', [None])[0]!=None:
                if query_components.get('scope', [None])[0]=='read':
                    # state is not MUST
                    if query_components.get('redirect_uri', [None])[0].startswith('http://localhost/'):
                        with open('template/authorize.html', 'r', encoding='utf-8') as file: # tuthorize grant UI
                            content = file.read()
                        sendSimpleResponse(context,200,content)
                    else:
                        sendSimpleResponse(context,400,"redirect_url is invalid.")
                else:
                    sendSimpleResponse(context,400,"scope is invalid")
            else:
                sendSimpleResponse(context,400,"state is invalid. require for prevent csrf attack")
        else:
            sendSimpleResponse(context,400,"client_id is invalid.")
    else:
        sendSimpleResponse(context,400,"response_type is invalid.")
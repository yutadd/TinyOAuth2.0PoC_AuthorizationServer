
from http.server import BaseHTTPRequestHandler


def authorize(context:BaseHTTPRequestHandler):
    pass
'''
4.1.1を参考に
クライアントからのパラメータを解析し、認可するかどうか確認するUIを返す。
チェックするパラメータは以下の通り。
response_type,client_id,state,redirect_uri
'''
def authorizeUI(context:BaseHTTPRequestHandler):
    username = context.headers.get('username')
    password = context.headers.get('password')
    context.send_response(200)
    context.send_header('Content-type', 'text/html; charset=utf-8')
    context.end_headers()
    with open('template/authorize.html', 'r', encoding='utf-8') as file:
        content = file.read()
    context.wfile.write(content.encode('utf-8'))

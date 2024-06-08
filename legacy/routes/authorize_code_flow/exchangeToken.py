from base64 import b64decode
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs

from util.CheckRequest import check_redirect_urls

from util.db.user import is_code_valid

from util.db.client import authenticate_client


def exchangeToken(context:BaseHTTPRequestHandler):
    query_components=parse_qs(context.rfile(context.headers['Content-Length']))
    grant_type=query_components.get('grant_type',[None])[0]
    code=query_components.get('code',[None])[0]
    success_redirect_url=query_components.get('success_redirect_url',[None])[0]
    fail_redirect_url=query_components.get('fail_redirect_url',[None])[0]
    authorization_header = context.headers.get('Authorization')
    credentials=b64decode(authorization_header.split(' ')[1]).split(':')
    if grant_type=='code':
        if check_redirect_urls([success_redirect_url,fail_redirect_url],credentials[0]):
            if authenticate_client(credentials[0],credentials[1]):
                if is_code_valid(code):
                    
                #TODO impl exchange to bearer
                    pass

from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs
from util.http import sendSimpleResponse
from util.registered import getClientById

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
    registeredClient=getClientById(query_components.get('client_id', [None])[0])
    if query_components.get('response_type', [None])[0] != 'code':
        sendSimpleResponse(context, 400, json.dumps({
            "error": "unsupported_response_type",
            "error_description": "The authorization server does not support obtaining an authorization code using this method."
        }))
        return
    if registeredClient==None:
        sendSimpleResponse(context, 400, json.dumps({
            "error": "invalid_client_id",
            "error_description": "The client is not authorized to request an authorization code using this method."
        }))
        return
    if query_components.get('state', [None])[0] is None:
        sendSimpleResponse(context, 400, json.dumps({
            "error": "invalid_request",
            "error_description": "The state parameter is required to prevent CSRF attacks."
        }))
        return

    if query_components.get('scope', [None])[0] != 'read':
        sendSimpleResponse(context, 400, json.dumps({
            "error": "invalid_scope",
            "error_description": "The requested scope is invalid, unknown, or malformed."
        }))
        return
    '''
    TODO リダイレクトURIが登録内容と違う場合、クライアントに通知し、自動的にリダイレクトしてはいけない。
    '''
    if not query_components.get('redirect_uri', [None])[0].startswith(registeredClient['redirect_uri']):
        sendSimpleResponse(context, 400, json.dumps({
            "error": "invalid_request",
            "error_description": "The redirect_uri is invalid."
        }))
        return

    with open('template/authorize.html', 'r', encoding='utf-8') as file:
        content = file.read()
    sendSimpleResponse(context, 200, content)
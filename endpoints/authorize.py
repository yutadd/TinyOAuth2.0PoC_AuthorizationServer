
from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs
from util.http import sendOAuth2ErrorResponseToClient,sendErrorResponseToUA, sendOAuth2SuccessResponse
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
    if context.headers.get('Content-Type') != 'application/x-www-form-urlencoded':
        sendErrorResponseToUA(context, 400, "invalid_request", "Content-Type must be application/x-www-form-urlencoded")
        return
    query_components = parse_qs(urlparse(context.path).query)
    registeredClient=getClientById(query_components.get('client_id', [None])[0])
    if registeredClient is None:
        sendErrorResponseToUA(context, 400, json.dumps({
            "error": "invalid_client_id",
            "error_description": "The client is not authorized to request an authorization code using this method."
        }))
        return
    redirect_uri = query_components.get('redirect_uri', [None])[0]
    if redirect_uri is None or not redirect_uri.startswith(registeredClient['redirect_uri']):
        sendErrorResponseToUA(context=context,statusCode=400, error="invalid_request",
                              error_description="The redirect_uri is invalid.")
        return
    if query_components.get('response_type', [None])[0] != 'code':
        sendOAuth2ErrorResponseToClient(context, 400, "unsupported_response_type", "The authorization server does not support obtaining an authorization code using this method.", redirect_uri, state)
        return
    if query_components.get('state', [None])[0] is None:
        sendOAuth2ErrorResponseToClient(context, 400, "invalid_request", "The state parameter is required to prevent CSRF attacks.", redirect_uri)
        return
    requested_scope = query_components.get('scope', [None])[0]
    if requested_scope is None or not set(requested_scope.split()).issubset(set(registeredClient['allowed_scopes'])):
        sendOAuth2ErrorResponseToClient(context, 400, json.dumps({
            "error": "invalid_scope",
            "error_description": "The requested scope is invalid, unknown, or malformed."
        }))
        return
    

    with open('template/authorize.html', 'r', encoding='utf-8') as file:
        content = file.read()
    # パラメータをHTMLに埋め込む
    content = content.replace('{{client_id}}', query_components.get('client_id', [''])[0])
    content = content.replace('{{response_type}}', query_components.get('response_type', [''])[0])
    content = content.replace('{{state}}', query_components.get('state', [''])[0])
    content = content.replace('{{redirect_uri}}', query_components.get('redirect_uri', [''])[0])
    content = content.replace('{{scope}}', query_components.get('scope', [''])[0])

    sendOAuth2SuccessResponse(context, 200, content)
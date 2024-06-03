#UI & login api
from http.server import BaseHTTPRequestHandler
from urllib import parse
from urllib.parse import urlparse, parse_qs

import bcrypt
from util.CheckRequest import  checkAuthorizationRequest
from util.db.client import getClientById
from util.assembleResponse import returnLoginUIToUA
from util.db.user import getUserByUsername

def checkAndSendAuthorizeUI(context: BaseHTTPRequestHandler):
    query_components = parse_qs(urlparse(context.path).query)
    registeredClient = getClientById(
    query_components.get('client_id', [None])[0])
    success_redirect_uri = query_components.get('success_redirect_uri', [None])[0]
    fail_redirect_uri = query_components.get('fail_redirect_uri', [None])[0]
    requested_scope = query_components.get('scope', [None])[0]
    client_provided_state = query_components.get('state', [None])[0]
    state = query_components.get('state', [None])[0]
    response_type=query_components.get('response_type', [None])[0]
    if checkAuthorizationRequest(context=context,success_redirect_uri=success_redirect_uri,client_provided_state=client_provided_state,fail_redirect_uri=fail_redirect_uri,registeredClient=registeredClient,requested_scope=requested_scope,response_type=response_type,response_type=response_type):
        returnLoginUIToUA(context=context,scope=requested_scope,fail_redirect_uri=fail_redirect_uri,client_id=registeredClient.client_id,success_redirect_uri=success_redirect_uri,response_type=response_type,state=state)
        
def processLogin(context: BaseHTTPRequestHandler):
    query_components = parse_qs(urlparse(context.path).query)
    registeredClient = getClientById(
    query_components.get('client_id', [None])[0])
    success_redirect_uri = query_components.get('success_redirect_uri', [None])[0]
    fail_redirect_uri = query_components.get('fail_redirect_uri', [None])[0]
    requested_scope = query_components.get('scope', [None])[0]
    client_provided_state = query_components.get('state', [None])[0]
    state = query_components.get('state', [None])[0]
    response_type=query_components.get('response_type', [None])[0]
    username=query_components.get('username', [None])[0]
    password=query_components.get('password', [None])[0]
    if checkAuthorizationRequest(context=context,success_redirect_uri=success_redirect_uri,client_provided_state=client_provided_state,fail_redirect_uri=fail_redirect_uri,registeredClient=registeredClient,requested_scope=requested_scope,response_type=response_type,response_type=response_type):
        returnLoginUIToUA(context=context,scope=requested_scope,fail_redirect_uri=fail_redirect_uri,client_id=registeredClient.client_id,success_redirect_uri=success_redirect_uri,response_type=response_type,state=state)
    if not authenticate(username, password):
        returnErrorUIToUA(context, "access_denied",
                          "Invalid username or password.")
        return False
    sendRedirectAndCodeToClient(context=context, success_redirect_uri=success_redirect_uri,
                                state=state, username=username)
def isloggedIn(context: BaseHTTPRequestHandler)->bool:
    pass

def authenticate(username: str, password: str)->bool:
    user = getUserByUsername(username)
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
        return True
    else:
        return False

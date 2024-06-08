

from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from util.CheckRequest import check_redirect_urls, checkAuthorizationRequest
from util.db.client import SearchClientByAnyColumn
from util.assembleResponse import returnAuthorizeUIToUA, returnErrorUIToUA, sendRedirectAndCodeToClient
from util.db.user import SearchUserByAnyColumn, check_loggedin_by_sessionid

'''
TODO:ここですべての引数をクエリから取り出すようにする
'''
'''
認可リクエスト
GET /authorize?response_type=code&client_id=s6BhdRkqt3&state=xyz
        &success_redirect_uri=http://localhost/authorize_success&fail_redirect_uri=http://localhost/authorize_fail HTTP/1.1
    Host: server.example.com
'''
def checkAndAuthorizeAndSendCode(context: BaseHTTPRequestHandler) -> bool:
    query_components = parse_qs(urlparse(context.path).query)
    registeredClient = SearchClientByAnyColumn('client_id',query_components.get('client_id', [None])[0])
    success_redirect_uri = query_components.get('success_redirect_uri', [None])[0]
    fail_redirect_uri = query_components.get('fail_redirect_uri', [None])[0]
    requested_scope = query_components.get('scope', [None])[0]
    state = query_components.get('state', [None])[0]
    response_type=query_components.get('response_type', [None])[0]
    session_id = context.headers.get('Cookie', '').split('AuthorizationServerSession_id=')[-1].split(';')[0]
    users=SearchUserByAnyColumn('session_id',session_id)
    if len(users)>0:
        user=users[0]
        if registeredClient is not None:
            if check_loggedin_by_sessionid(session_id):
                if check_redirect_urls([success_redirect_uri,fail_redirect_uri],registeredClient.client_id):
                    if response_type=='code':
                        sendRedirectAndCodeToClient(context=context, success_redirect_uri=success_redirect_uri,
                            state=state,username=user.username)
    else:
        returnErrorUIToUA(context,"invalid_*","Not Implemented yet")# TODO: impl error messages
def SendAuthorizationUI(context: BaseHTTPRequestHandler):
    query_components = parse_qs(urlparse(context.path).query)
    client_id=query_components.get('client_id', [None])[0]
    success_redirect_uri = query_components.get(
        'success_redirect_uri', [None])[0]
    fail_redirect_uri = query_components.get('fail_redirect_uri', [None])[0]
    requested_scope = query_components.get('scope', [None])[0]
    state = query_components.get('state', [None])[0]
    response_type = query_components.get('response_type', [None])[0]
    returnAuthorizeUIToUA(context=context,client_id=client_id,fail_redirect_uri=fail_redirect_uri,response_type=response_type,scope=requested_scope,state=state,success_redirect_uri=success_redirect_uri)
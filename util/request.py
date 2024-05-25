from http.server import BaseHTTPRequestHandler

from util.http import returnErrorUIToUA, sendRedirectAndErrorToClient
from util.registered import getClientById


def checkParam(context:BaseHTTPRequestHandler,query_components:dict[str, list[str]])->bool:
    registeredClient=getClientById(query_components.get('client_id', [None])[0])
    state=query_components.get('state', [None])[0]
    if registeredClient is None:
        returnErrorUIToUA(context, "invalid_client_id",
             "The client is not authorized to request an authorization code using this method."
        )
        return
    redirect_uri = query_components.get('redirect_uri', [None])[0]
    if redirect_uri is None or not redirect_uri.startswith(registeredClient['redirect_uri']):
        returnErrorUIToUA(context=context, error="invalid_request",
                              error_description="The redirect_uri is invalid.")
        return False
    if state is None:
        returnErrorUIToUA(context, "invalid_request", "The state parameter is required to prevent CSRF attacks.", )
        return False
    if query_components.get('response_type', [None])[0] != 'code':
        sendRedirectAndErrorToClient(context, "unsupported_response_type", "The authorization server does not support obtaining an authorization code using this method.", redirect_uri, state)
        return False

    requested_scope = query_components.get('scope', [None])[0]
    if requested_scope is None or not set(requested_scope.split()).issubset(set(registeredClient['allowed_scopes'])):
        sendRedirectAndErrorToClient(context, "invalid_scope", "The requested scope is invalid, unknown, or malformed.",redirect_uri=redirect_uri,state=state)
        return False
    return True
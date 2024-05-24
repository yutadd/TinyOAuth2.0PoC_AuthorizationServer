from http.server import BaseHTTPRequestHandler
import json
def sendOAuth2SuccessResponse(context: BaseHTTPRequestHandler, statusCode: int, data: dict):
    context.send_response(statusCode)
    context.send_header('Content-Type', 'application/json')
    context.end_headers()
    response = {
        'status': 'success',
        'data': data
    }
    context.wfile.write(bytes(json.dumps(response), 'utf-8'))

def sendOAuth2ErrorResponseToClient(context: BaseHTTPRequestHandler, statusCode: int, error: str, error_description: str = '', redirect_uri: str = None, state: str = None):
    if redirect_uri:
        # エラーメッセージをリダイレクトURIに含める
        error_response = f"{redirect_uri}?error={error}&error_description={error_description}"
        if state:
            error_response += f"&state={state}"
        context.send_response(302)
        context.send_header('Location', error_response)
        context.end_headers()
    else:
        context.send_response(statusCode)
        context.send_header('Content-Type', 'application/json')
        context.end_headers()
        response = {
            'error': error,
            'error_description': error_description
        }
        context.wfile.write(bytes(json.dumps(response), 'utf-8'))
def sendErrorResponseToUA(context: BaseHTTPRequestHandler, statusCode: int, error: str, error_description: str = ''):
    context.send_response(statusCode)
    context.send_header('Content-Type', 'application/json')
    context.end_headers()
    response = {
        'error': error,
        'error_description': error_description
    }
    context.wfile.write(bytes(json.dumps(response), 'utf-8'))
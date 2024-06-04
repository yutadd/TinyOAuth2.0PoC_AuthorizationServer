from http.server import BaseHTTPRequestHandler

from util.db.user import issue_Authorization_Code
# クライアント認証は、basic認証で、usernameには、クライアントIDを使用し、passwordにはclient_secretを使用する。
def returnAuthenticateUIToUA(context: BaseHTTPRequestHandler,client_id,response_type,state,success_redirect_uri,fail_redirect_uri,scope):
    with open('template/authenticate.html', 'r', encoding='utf-8') as file:
        content = file.read()
    # パラメータをHTMLに埋め込む
    content = content.replace('{{client_id}}', client_id)
    content = content.replace('{{response_type}}', response_type)
    content = content.replace('{{state}}', state)
    content = content.replace('{{success_redirect_uri}}', success_redirect_uri)
    content = content.replace('{{fail_redirect_uri}}', fail_redirect_uri)
    content = content.replace('{{scope}}', scope)
    context.send_response(200)
    context.send_header('Content-Type', 'text/html; charset=utf-8')
    context.end_headers()
    context.wfile.write(bytes(content, 'utf-8'))
def returnAuthorizeUIToUA(context: BaseHTTPRequestHandler,client_id:str,response_type:str,state:str,success_redirect_uri:str,fail_redirect_uri:str,scope:str):
    with open('template/authorize.html', 'r', encoding='utf-8') as file:
        content = file.read()
    # パラメータをHTMLに埋め込む
    content = content.replace('{{client_id}}', client_id)
    content = content.replace('{{response_type}}', response_type)
    content = content.replace('{{state}}', state)
    content = content.replace('{{success_redirect_uri}}', success_redirect_uri)
    content = content.replace('{{fail_redirect_uri}}', fail_redirect_uri)
    content = content.replace('{{scope}}', scope)
    context.send_response(200)
    context.send_header('Content-Type', 'text/html; charset=utf-8')
    context.end_headers()
    context.wfile.write(bytes(content, 'utf-8'))

def returnErrorUIToUA(context: BaseHTTPRequestHandler,error:str,error_detail:str):
    with open('template/error.html', 'r', encoding='utf-8') as file:
        content = file.read()
    content = content.replace('{{error}}', error)
    content = content.replace('{{error_detail}}', error_detail)
    context.send_response(400)
    context.send_header('Content-Type', 'text/html; charset=utf-8')
    context.end_headers()
    context.wfile.write(bytes(content, 'utf-8'))
'''
エラー応答
HTTP/1.1 302 Found
   Location: https://client.example.com/cb?error=access_denied&state=xyz
'''
def sendRedirectAndErrorToClient(context: BaseHTTPRequestHandler,  error: str, error_description: str, redirect_uri: str , state: str ):
    # エラーメッセージをリダイレクトURIに含める
    error_response = f"{redirect_uri}?error={error}&error_description={error_description}"
    if state:
        error_response += f"&state={state}"
    context.send_response(302)
    context.send_header('Location', error_response)
    context.end_headers()
    '''
    認可応答
     HTTP/1.1 302 Found
     Location: https://client.example.com/cb?code=SplxlOBeZQQYbYS6WxSbIA
               &state=xyz
    '''
def sendRedirectAndCodeToClient(context: BaseHTTPRequestHandler, success_redirect_uri: str , state: str ,username:str):
# TODO codeの時間制限を実装する
    success_response = f"{success_redirect_uri}?code={issue_Authorization_Code(username)}"
    if state:
        success_response += f"&state={state}"
    context.send_response(302)
    context.send_header('Location', success_response)
    context.end_headers()
'''
Access Token Response
  {
       "access_token":"2YotnFZFEjr1zCsicMWpAA",
       "token_type":"example",
       "expires_in":3600,
       "refresh_token":"tGzv3JOkF0XG5Qx2TlKWIA",
       "example_parameter":"example_value"
     }
'''
def sendRedirectAndTokenToClient(context:BaseHTTPRequestHandler,code:str,redirect_uri:str,state:str):
    # TODO codeの時間制限を実装する
    success_response = f"{redirect_uri}?access_token={issue_Authorization_Code(code)}"
    if state:
        success_response += f"&state={state}"
    context.send_response(302)
    context.send_header('Location', success_response)
    context.end_headers()
def return_sessionId_and_redirect(context: BaseHTTPRequestHandler, session_id: str,post_data:str):
    # クッキーの設定
    context.send_response(302)
    paramstr = post_data.decode('utf-8')
    cookie = f"session_id={session_id}; HttpOnly; Path=/"
    context.send_header('Set-Cookie', cookie)
    context.send_header('Location', f'http://localhost:8080/authorize/ask/authorize?{paramstr}')
    context.end_headers()


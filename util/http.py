from http.server import BaseHTTPRequestHandler

from util.user import issue_Authorization_Code
def returnLoginUIToUA(context: BaseHTTPRequestHandler,query_components: dict[str, list[str]]):
    with open('template/authorize.html', 'r', encoding='utf-8') as file:
        content = file.read()
    # パラメータをHTMLに埋め込む
    content = content.replace('{{client_id}}', query_components.get('client_id', [''])[0])
    content = content.replace('{{response_type}}', query_components.get('response_type', [''])[0])
    content = content.replace('{{state}}', query_components.get('state', [''])[0])
    content = content.replace('{{redirect_uri}}', query_components.get('redirect_uri', [''])[0])
    content = content.replace('{{scope}}', query_components.get('scope', [''])[0])
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
def sendRedirectAndCodeToClient(context: BaseHTTPRequestHandler, redirect_uri: str , state: str ,username):
# TODO codeの時間制限を実装する
    success_response = f"{redirect_uri}?code={issue_Authorization_Code(username)}"
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

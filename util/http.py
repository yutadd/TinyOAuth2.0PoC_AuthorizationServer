from http.server import BaseHTTPRequestHandler


def sendSimpleResponse(context: BaseHTTPRequestHandler,statusCode:int,text:str):
    context.send_response(statusCode)
    context.send_header('x-frame-options','deny')
    context.send_header('Content-type', 'text/html; charset=utf-8')
    context.end_headers()
    context.wfile.write(bytes(text,'utf-8'))
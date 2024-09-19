from machine import Pin
import network
import socket
import time
from func import *

# Configuração da rede Wi-Fi
ssid = 'lab8'
password = 'lab8arduino'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

icon = bytearray([
    0x00, 0x03, 0xc0, 0x00, 0x00, 0x03, 0xc0, 0x00, 0x00, 0x03, 0xc0, 0x00, 0x00, 0x7f, 0xfe, 0x00, 
    0x00, 0xff, 0xff, 0x00, 0x01, 0xff, 0xff, 0x80, 0x03, 0xff, 0xff, 0xc0, 0x03, 0xc3, 0xc3, 0xc0, 
    0x07, 0xc3, 0xc3, 0xe0, 0x07, 0x83, 0xc1, 0xe0, 0x07, 0x83, 0xc1, 0xc0, 0x03, 0xc3, 0xc0, 0x00, 
    0x03, 0xe3, 0xc0, 0x00, 0x03, 0xff, 0xc0, 0x00, 0x01, 0xff, 0xc0, 0x00, 0x00, 0xff, 0xfc, 0x00, 
    0x00, 0x3f, 0xff, 0x00, 0x00, 0x03, 0xff, 0x80, 0x00, 0x03, 0xff, 0xc0, 0x00, 0x03, 0xc7, 0xc0, 
    0x00, 0x03, 0xc3, 0xc0, 0x03, 0x83, 0xc1, 0xe0, 0x07, 0x83, 0xc1, 0xe0, 0x07, 0xc3, 0xc3, 0xe0, 
    0x03, 0xc3, 0xc3, 0xc0, 0x03, 0xff, 0xff, 0xc0, 0x01, 0xff, 0xff, 0x80, 0x00, 0xff, 0xff, 0x00, 
    0x00, 0x7f, 0xfe, 0x00, 0x00, 0x03, 0xc0, 0x00, 0x00, 0x03, 0xc0, 0x00, 0x00, 0x03, 0xc0, 0x00
])

# Aguarda até que a conexão seja estabelecida
while not wlan.isconnected():
    time.sleep(1)

print('Conectado à rede Wi-Fi')
print('Endereço IP:', wlan.ifconfig()[0])

def handle_request(client):
    try:
        request = client.recv(1024).decode('utf-8')
        print('Requisição recebida:')
        print(request)
        
        if 'GET / ' in request:
            response = """\
HTTP/1.1 200 OK\r
Content-Type: text/html\r
\r
<!DOCTYPE html>
<html>
<head>
    <title>ESP32 Web Server</title>
</head>
<body>
    <h1>Bem-vindo ao Servidor ESP32</h1>
    <p>Visite <a href="/hello">/hello</a> ou <a href="/status">/status</a></p>
</body>
</html>
"""
        elif 'GET /hello ' in request:
            response = """\
HTTP/1.1 200 OK\r
Content-Type: text/html\r
\r
<!DOCTYPE html>
<html>
<head>
    <title>Olá!</title>
</head>
<body>
    <h1>Olá, Mundo!</h1>
    <p>Esta é a página /hello.</p>
</body>
</html>
"""
        elif 'GET /dinheiro ' in request:
            Dinheiro(icon)
            response = """\
HTTP/1.1 200 OK\r
Content-Type: text/html\r
\r
<!DOCTYPE html>
<html>
<head>
    <title>ESP32 Web Server</title>
</head>
<body>
    <h1>TOMA SEU DINHEIRO!</h1>
    <p>Limpe a tela: <a href="/clear">/limpar a tela</a></p>
</body>
</html>
"""
        elif 'GET /clear ' in request:
            Clear()
            response = """\
HTTP/1.1 200 OK\r
Content-Type: text/html\r
\r
<!DOCTYPE html>
<html>
<head>
    <title>ESP32 Web Server</title>
</head>
<body>
    <h1>Tela limpa!</h1>
    <p>Quer mais <a href="/dinheiro">/DINHEIRO???</a></p>
</body>
</html>
"""
        elif 'GET /status ' in request:
            response = """\
HTTP/1.1 200 OK\r
Content-Type: text/html\r
\r
<!DOCTYPE html>
<html>
<head>
    <title>Status</title>
</head>
<body>
    <h1>Status do Servidor</h1>
    <p>O servidor está funcionando corretamente.</p>
</body>
</html>
"""
        else:
            response = """\
HTTP/1.1 404 Not Found\r
Content-Type: text/html\r
\r
<!DOCTYPE html>
<html>
<head>
    <title>404 Not Found</title>
</head>
<body>
    <h1>404 - Página não encontrada</h1>
</body>
</html>
"""

        client.send(response)
    except Exception as e:
        print("Erro ao processar requisição:", e)
        response = """\
HTTP/1.1 500 Internal Server Error\r
Content-Type: text/html\r
\r
<!DOCTYPE html>
<html>
<head>
    <title>500 Internal Server Error</title>
</head>
<body>
    <h1>500 - Erro Interno do Servidor</h1>
</body>
</html>
"""
        client.send(response)
    finally:
        client.close()

# Configuração do servidor TCP
s = None
try:
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    print('Servidor escutando na porta 80...')

    while True:
        client, addr = s.accept()
        print('Cliente conectado de', addr)
        handle_request(client)
except OSError as e:
    print("Erro de servidor:", e)
finally:
    if s:
        try:
            s.close()
        except Exception as e:
            print("Erro ao fechar o socket:", e)


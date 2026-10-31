import json
import socket

host = '127.0.0.1'
port = 8081
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()

while True:
    conn, addr = server_socket.accept()
    data = conn.recv(1024).decode('utf-8')
    print(data)
    splitting = data.split()
    if len(splitting) >= 2:
        path = splitting[1]
        method = splitting[0]
        http_info = {
            'method': method,
            'path': path,
            'headers': {},
            'request-body': None,
            'Content-Type': 'text/html',
            'Connection': 'close',
            'id': id,
            # 'name': name,
            'status' : 'success',
        }
        if method == 'GET':
            path = path.lstrip('/')
            if  path == '' or path == 'index.html':
                try:
                    with open(path, 'rb') as file:
                        content = file.read()
                    response = f'HTTP/1.1 200 OK\n Content-Type: text/html '.encode('utf-8') + content
                    conn.sendall(response)
                    conn.close()
                except FileNotFoundError:
                    conn.sendall(b'HTTP/1.1 404 Not Found\n')
                    conn.send(b'Connection: close\n')
                    conn.close()
        elif method == 'POST':
            http_info['request-body'] = data
            if path == '/json':
                try:
                    content = json.dumps(http_info['request-body'])
                    response = f'HTTP/1.1  201 CREATED\n Content-Type: application/json\n'.encode('utf-8') + content.encode('utf-8')
                    conn.sendall(response)
                    conn.close()
                except FileNotFoundError:
                    conn.sendall(b'HTTP/1.1 404 Not Found\n')
                    conn.send(b'Connection: close\n')
                    conn.close()






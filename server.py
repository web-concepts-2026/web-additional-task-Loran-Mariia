import json
import socket
from urllib.parse import urlparse, parse_qs

host = '127.0.0.1'
port = 8081
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((host, port))
server_socket.listen()
print(f"Server is running on http: //{host}:{port}")

while True:
    client_connection = server_socket.accept()
    conn = client_connection[0]
    addr = client_connection[1]
    data = conn.recv(1024).decode('utf-8')
    if not data:
        conn.close()
        continue

    print(data)
    if '\r\n\r\n' in data:
        parts = data.split('\r\n\r\n', 1)
        header_part = parts[0]
        if len(parts) > 1:
            body = parts[1]
        else:
            body = ''
    else:
        header_part = data
        body = ''
    header_lines = header_part.split('\r\n')
    if not header_lines:
        conn.close()
        continue
    request_line = header_lines[0]
    splitting = request_line.split()

    if len(splitting) >= 2:
        method = splitting[0]
        path = splitting[1]

        parser_url = urlparse(path)
        path = parser_url.path
        query = parse_qs(parser_url.query)

        headers_dict = {}
        for line in header_lines[1:]:
            if ':' in  line :
                parts_dict = line.split(':', 1)
                key = parts_dict[0]
                value = parts_dict[1]
                headers_dict[key.strip().lower()] = value.strip()
        if method == 'GET':
            clean_path = path.lstrip('/')
            if  clean_path == '' or clean_path == 'index.html':
                filename = 'index.html'
            else:
                filename = clean_path

            try:
                with open(filename, 'rb') as file:
                    content = file.read()
                response_header = 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8\r\n\r\n'
                conn.sendall(response_header.encode('utf-8')  + content)
            except FileNotFoundError:
                conn.sendall(b'HTTP/1.1 404 Not Found\r\nConnection: close\r\n\r\n')
        elif method == 'POST':
            if path == '/json' or path == '/':
                response_data = {
                    'status': 'success',
                    'message': 'POST request received',
                    'headers': headers_dict,
                    'received-body': body,
                    'query': query
                }
                content = json.dumps(response_data)
                content_bytes = content.encode('utf-8')
                response_header = (
                    "HTTP/1.1  201 CREATED\r\n"
                    "Content-Type: application/json; charset=utf-8\r\n"
                    f"Content-Length: {len(content_bytes)}\r\n"
                    "\r\n"
                )
                conn.sendall(response_header.encode('utf-8')  + content_bytes)
            else:
                conn.sendall(b'HTTP/1.1 404 Not Found\r\nConnection: close\r\n\r\n')
    conn.close()






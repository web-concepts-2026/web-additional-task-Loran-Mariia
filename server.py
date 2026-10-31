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

        if method == 'GET':
            conn.send(b'HTTP/1.1 200 OK\n')
        elif method == 'POST':
            conn.send(b'HTTP/1.1 201 CREATED\n')
            conn.send(b'Content-Type: text/html\n')
            conn.send(b'Connection: close\n')
            conn.send(b'\n')





import socket

HOST = '127.0.0.1'
PORT = 21

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Server Listening")
    connection, client = s.accept()
    with connection:
        print("Connection Recieved from:", client)
        connection.sendall("Hello World".encode())

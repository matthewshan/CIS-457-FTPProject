import socket
import os

HOST = '127.0.0.1'
PORT = 21

# THIS IS THE CORRECT FILE


# Used for RETRIEVE
def send_file(connection, filename):
    pass

# Used for STORE
def receive_file(connection, filename, filesize):
    to_write = open(filename, "wb")
    to_write.write(connection.recv(int(filesize)))
    connection.sendall("File written".encode())


# Used for LIST
def list_files(connection):
    cwd = os.getcwd()
    files = os.listdir(cwd)
    toSend = "====Files on Server====\n"
    toSend += "\n".join(files)
    toSend += "\n======================="
    connection.sendall(toSend.encode())


# Do the work of creating a connection and receiving commands
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Server Listening")
    connection, client = s.accept()
    with connection:
        while(True):
            rData = connection.recv(1024).decode()
            connection.sendall(("Received command: " + rData).encode())
    
            # If the command given is QUIT, send a goodbye to the client and terminate the connection
            if rData == "QUIT":
                connection.sendall("Bye bye".encode())
                break
            # If the command given is LIST, execute our list_files function
            elif rData == "LIST":
                list_files(connection)
                continue 
            # Differentiate between STORE and RECEIVE
            rData = rData.split(" ")

            # If the command given is STORE, get ready to accept a file
            if rData[0] == "STORE":
                receive_file(connection, rData[1], rData[2])
            elif rData[0] == "RETRIEVE":
                send_file(connection, rData[1])
            else:
                connection.sendall("Invalid command! Valid commands: QUIT, LIST, STORE, RETRIEVE".encode())
            print("Client sent: ", rData)
            # connection.sendall(rData.encode())
            #print("Connection Recieved from:", client)
            #connection.sendall("Hello World".encode())

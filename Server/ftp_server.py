import socket, os, math

HOST = '127.0.0.1'
PORT = 2000

# THIS IS THE CORRECT FILE

# RETRIEVE s, s(n)
def send_file(connection, filename):
    #Check to see of the file is on the server
    try:
        size = os.path.getsize("./" + filename)
    except:
        print("File does not exists. Returning")
        connection.sendall("ERROR".encode())
        return

    # Send the size of the file 
    print("Size of file being sent: ", size)
    connection.sendall(str(size).encode())
    my_file = open(filename, 'rb')

    #Start sending the file
    line = my_file.read(1024)
    payload = line
    while(line):
        line = my_file.read(1024)
        payload += line
    connection.sendall(payload)
    my_file.close()

# STORE [r], r(n), s
def accept_file(connection, filename, filesize):

    # Write the file 
    to_write = open(filename, "wb")
    print("Expected number of transfers: ", math.ceil(int(filesize)/1024))
    """ for i in range(math.ceil(int(filesize)/1024)):
        to_write.write(connection.recv(1024)) 
        print(i) #TODO: Delete """
    payload = connection.recv(int(filesize), socket.MSG_WAITALL)
    to_write.write(payload) 
    to_write.close()

    #Send confirmation
    connection.sendall("File written".encode())


# LIST
def list_files(connection):
    cwd = os.getcwd()
    files = os.listdir(cwd)
    toSend = "====Files on Server====\n"
    toSend += "\n".join(files)
    toSend += "\n======================="
    connection.sendall(toSend.encode())


# Entry point of the program
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Server Listening")
    connection, client = s.accept()
    with connection:
        while(True):
            print("\nAwaiting new command")
            rData = connection.recv(1024).decode()
            print("Client sent: ", rData)
            if rData == '':
                continue
    
            # If the command given is QUIT, send a goodbye to the client and terminate the connection
            if rData == "QUIT":
                print("Bye Bye")
                connection.sendall("\nBye bye".encode())
                break
            # If the command given is LIST, execute our list_files function
            elif rData == "LIST":
                list_files(connection)
            else:
                # Differentiate between STORE and RECEIVE
                rData = rData.split(" ")

                # If the command given is STORE, get ready to accept a file
                if rData[0] == "STORE":
                    accept_file(connection, rData[1], rData[2])
                elif rData[0] == "RETRIEVE":
                    send_file(connection, rData[1])
                else:
                    connection.sendall("Invalid command! Valid commands: QUIT, LIST, STORE, RETRIEVE".encode())
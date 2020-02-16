import socket, os, math, sys

class Connection():
    def __init__(self):
        self.connected = False

    def connect(self, ip, port):
        self.connected = True
        self.HOST = ip
        self.PORT = port
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.HOST, self.PORT))

    def test(self):
        self.conn.sendall("This is a test".encode())
        data = self.conn.recv(1024)

        print(data.decode("utf-8"))

    def list_files(self):
        self.conn.sendall("LIST".encode())
        #print(self.conn.recv(1024).decode())
        print(self.conn.recv(1024).decode())
    
    def close(self):    
        self.conn.sendall("QUIT".encode())
        #print(self.conn.recv(1024).decode())
        print(self.conn.recv(1024).decode())
        self.conn.close()
    
    def retrieve(self, filename):
        self.conn.sendall(("RETRIEVE " + filename).encode())
        #print(self.conn.recv(1024).decode())
        to_write = open(filename, "wb")
        filesize = self.conn.recv(1024).decode('utf-8')
        print(filesize)
        print("Expected number of transfers: ", math.ceil(int(filesize)/1024))
        for i in range(math.ceil(int(filesize)/1024)):
            to_write.write(self.conn.recv(1024))
            print(i)
        to_write.close()
        print("File received!")

    def store(self, filename):
        size = os.path.getsize("./" + filename)
        self.conn.sendall(("STORE " + filename  + " " + str(size)).encode())
        #print(self.conn.recv(1024).decode())

        my_file = open(filename, 'rb')
        line = my_file.read(1024)
        i = 0
        while(line):
            print(i)
            i += 1
            self.conn.sendall(line)
            line = my_file.read(1024)
        my_file.close()
        
        print(self.conn.recv(1024).decode())
        

connection = Connection()
while True:
    commands = str(input("\nftp> "))
    commands = commands.split(" ")
    if(len(commands) == 0):
        print("Invalid command, please try again")
    else:
        if commands[0] == "CONNECT":
            if len(commands) == 1:
                commands.append("localhost")
                commands.append("21")
            connection.connect(commands[1], int(commands[2]))
            print("Connection Formed with " + commands[1] + ":" + commands[2])
        elif commands[0] == "LIST":
            connection.list_files()
        elif commands[0] == "RETRIEVE":
            connection.retrieve(commands[1])
        elif commands[0] == "STORE":
            connection.store(commands[1])
        elif commands[0] == "QUIT":
            connection.close()
            break
        elif commands[0] == "TEST":
            connection.test()
        else:
            print("Invalid command")

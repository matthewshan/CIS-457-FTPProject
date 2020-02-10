import socket
import sys

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
        data = self.conn.recv(1024)
        self.conn.close()

        print(data.decode("utf-8"))
    
    def close(self):
        self.conn.close()

done = False
connection = Connection()
while True:
    commands = str(raw_input("ftp> "))
    commands = commands.split(" ")
    if(len(commands) == 0):
        print("Invalid command, please try again")
    else:
        if commands[0] == "CONNECT":
            connection.connect(commands[1], int(commands[2]))
            print("Connection Formed with " + commands[1] + ":" + commands[2])
        elif commands[0] == "LIST":
            print("list")
        elif commands[0] == "RETRIEVE":
            print("retrieve")
        elif commands[0] == "STORE":
            print("store")
        elif commands[0] == "QUIT":
            connection.close()
            break
        elif commands[0] == "TEST":
            connection.test()
        else:
            print("Invalid command")

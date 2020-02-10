import socket
import sys

class Connection():
    def __init__(self, ip, port):
        self.HOST = ip
        self.PORT = port
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((HOST, PORT))

    def test(self):
        data = s.recv(1024)
        s.close()

        print(data.decode("utf-8"))

done = False
socket = None
while not done:
    if(len(sys.argv) < 2):
        print("Invalid command, please try again")
    else:
        command = sys.argv[1]
        if command == "CONNECT":
            socket = Connection(sys.argv[2], sys.argv[3])
        elif command == "LIST":
            print("list")
        elif command == "RETRIEVE":
            print("retrieve")
        elif command == "STORE":
            print("store")
        elif command == "QUIT":
            print("quit")
        elif command == "TEST":
            socket.test()
        else:
            print("Invalid command")





import socket, os, math, sys, traceback

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
        print(self.conn.recv(1024).decode())
    
    def close(self):    
        self.conn.sendall("QUIT".encode())
        print(self.conn.recv(1024).decode())
        self.conn.close()
    
    # RETRIEVE [s], r, r(n)
    def retrieve(self, filename):
        #Send the initial
        self.conn.sendall(("RETRIEVE " + filename).encode())

        #Checks to see if the server is ready
        code = self.conn.recv(1024).decode()
        if(code == "ERROR"):
            print("Issue openning that file. Make sure that it is on the server")
            return

        #Start writing the file
        to_write = open(filename, "wb")
        filesize = code
        print("File size to receive: ", filesize)
        payload = self.conn.recv(int(filesize), socket.MSG_WAITALL)
        to_write.write(payload) 
        to_write.close()
        print("File written")

    # STORE
    def store(self, filename):
        #Checks to see if the file exists before sending requests
        try: 
            size = os.path.getsize("./" + filename)
        except FileNotFoundError:
            print("File not found. Please try again")
            return

        #Sends are store request
        self.conn.sendall(("STORE " + filename  + " " + str(size)).encode())

        # When ready, 
        my_file = open(filename, 'rb')
        line = my_file.read(int(size))
        file_load = line
        while(line):
            line = my_file.read(int(size))
            file_load += line
        self.conn.sendall(file_load)

        my_file.close()
        
        # Recieve confirmation
        print(self.conn.recv(1024).decode())
        

connection = Connection()
try:
    cli = "\nftp> "
    while True:
        commands = str(input(cli))
        commands = commands.split(" ")
        commands[0] = commands[0].upper() 
        if(len(commands) == 0):
            print("Invalid command, please try again")
            continue

        if connection.connected:
            if commands[0] == "LIST":
                connection.list_files()
            elif commands[0] == "RETRIEVE":
                connection.retrieve(commands[1])
            elif commands[0] == "STORE":
                connection.store(commands[1])
            elif commands[0] == "QUIT":
                connection.close()
                connection = Connection()
                break
            else:
                print("Invalid command! Valid commands: QUIT, LIST, STORE, RETRIEVE")
        else:        
            if commands[0] == "CONNECT":
                try:
                    if len(commands) == 1:
                        commands.append("localhost")
                        commands.append("21")
                    connection.connect(commands[1], int(commands[2]))
                    print("Connection Formed with " + commands[1] + ":" + commands[2])
                    cli =  "\n[" + commands[1] + ":" + commands[2] + "] ftp> "
                except:
                    connection = Connection()
                    print("There was an issue connecting. Retry.")
            else:
                print("Please CONNECT to a server before preforming commands")
except:
    connection.close()
    traceback.print_exc(file=sys.stdout)

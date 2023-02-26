import socket
import threading

host = "localhost"
port = 666

server = socket.socket()
server.bind((host, port))
server.listen(10)
client = []

def start():
    while True:
        conn, addr = server.accept()
        client.append(conn)
        #name = conn.recv(48)
        #print(name)
        print(f"Connected: {addr}")
        t = threading.Thread(target = send, args = (conn, ))
        t.start()

def send(fromConnection):
        while True:
            data = fromConnection.recv(48)
            for cl in client:
                if cl != fromConnection:
                    cl.send(data)
        print("out")
        fromConnection.close()
start()
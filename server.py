import socket
import sys
from thread import start_new_thread

HOST = ''
PORT = 9999

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    print("Could not create socket. Error Code: ", str(msg[0]), "Error: ", msg[1])
    sys.exit(0)

print("[-] Socket Created")


try:
    s.bind((HOST, PORT))
    print("[-] Socket Bound to port " + str(PORT))
except socket.error, msg:
    print("Bind Failed. Error Code: {} Error: {}".format(str(msg[0]), msg[1]))
    sys.exit()

s.listen(10)
print("Listening...")

def client_thread(conn):
    conn.send("Welcome to the Server.\n")

    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(data)
        reply = "message from server"
        conn.sendall(reply)
    conn.close()

while True:
    conn, addr = s.accept()
    print("[-] Connected to " + addr[0] + ":" + str(addr[1]))

    start_new_thread(client_thread, (conn,))

s.close()

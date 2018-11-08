import socket

HOST = '0.0.0.0'
PORT = 9999

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

client.send('hello from client')

while True:
    response = client.recv(4096)
    print response

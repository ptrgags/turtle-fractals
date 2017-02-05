#!/usr/bin/env python
import sys
import socket
ADDR = ('localhost', 3000)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_socket.connect(ADDR)
print("Connected!")

ack = client_socket.recv(8192)
if ack.startswith("Sorry"):
    print("Connection rejected by server.")
    sys.exit(0)

try:
    while True:
        message = raw_input("message> ").strip()
        client_socket.sendall("{0}\n".format(message))
        print(client_socket.recv(8192))
except socket.error:
    print("Whoops! something went wrong with our connection to the server.")
    sys.exit(1)

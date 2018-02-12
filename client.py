import socket
import sys

s = socket.socket()
s.connect(("localhost",8228))
f = open ("C://server//lol.ls", "rb")
l = f.read(1024)
while (l):
    s.send(l)
    l = f.read(1024)
s.close()
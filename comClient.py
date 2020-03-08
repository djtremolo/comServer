import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 50000))
s.sendall(str.encode(sys.argv[1]))
data = s.recv(1024)
s.close()
print ('Received', repr(data))
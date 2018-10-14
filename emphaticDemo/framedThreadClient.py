#! /usr/bin/env python3

# Echo client program
import socket, sys, re
from framedSock import FramedStreamSock
from threading import Thread
import time

server, usage, debug  = "localhost:50001", False, False

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

class ClientThread(Thread):
    def __init__(self, serverHost, serverPort, debug, file_name):
        Thread.__init__(self, daemon=False)
        self.serverHost, self.serverPort, self.debug = serverHost, serverPort, debug
        self.start()
    def run(self):
       s = None
       for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_INET, socket.SOCK_STREAM):
           af, socktype, proto, canonname, sa = res
           sa = ('127.0.0.1', 50001)
           try:
               print("Creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
               s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
           except socket.error as msg:
               print(" error: %s" % msg)
               s = None
               continue
           try:
               print("Attempting to connect to %s" % repr(sa))
               s.connect(sa)
               print("Connected to server.")
           except socket.error as msg:
               print("Error: ", msg)
               s.close()
               s = None
               continue
           break

       if s is None:
           print('could not open socket')
           sys.exit(1)

       fs = FramedStreamSock(s, debug=debug)
       try:
           with open(file_name, "r") as clientFile:
               print("Sending data...")
               data = clientFile.read()
               print("Data = ", data[:90])
               s.send(data.encode())
               #print("Data sent.")
               #print("Waiting for data...")
               #print("received: ", s.recv(100))
               clientFile.close()
       except IOError as e:
           print("No such file or directory.")
       print("Successfully sent file to server.")

print("--- File Transfer ---")
file_name = input("Enter name of file to send: ")
for i in range(5):
    ClientThread(serverHost, serverPort, debug, file_name)

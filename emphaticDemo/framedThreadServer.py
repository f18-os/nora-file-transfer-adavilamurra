#! /usr/bin/env python3
import sys, os, socket, params, time
from threading import Thread
from framedSock import FramedStreamSock

debug, listenPort = False, 50001

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

class ServerThread(Thread):
    requestCount = 0            # one instance / class
    def __init__(self, sock, debug, nameVar):
        Thread.__init__(self, daemon=True)
        self.fsock, self.debug = FramedStreamSock(sock, debug), debug
        self.sock = sock
        self.start()
    def run(self):
        with open("outputFile.txt", "w") as serverFile:
            while True:
                print("Receiving data...")
                msg = self.sock.recv(100).decode()
                print("Data received: ", msg)
                if not msg or msg is None:
                    print("End of file.")
                    break
                serverFile.write(msg)
                requestNum = ServerThread.requestCount
                #lock = Thread.Lock()
                #lock.acquire()
                #with lock:
                #    print("Locking thread.")
                #    time.sleep(0.1)
                ServerThread.requestCount = requestNum + 1
                #msg = ("%s! (%d)" % (msg, requestNum)).encode()
                #print("Sending data = ", msg.decode())
                #self.sock.send(msg)
                #print("Data sent.\n\n")
        serverFile.close()
        print("Successfully got file from client")
nameVar = 1
while True:
    sock, addr = lsock.accept()
    print("Got connection from ", addr)
    ServerThread(sock, debug, nameVar)
    nameVar = nameVar + 1

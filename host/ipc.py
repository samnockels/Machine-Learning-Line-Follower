"""
IPC
Inter Process Communication class built using sockets. Allows 
sending messages between rover (running python 2.7) and computer 
running python 3.

Data Flow:
          
      -> [pixy data]  ->  
Rover                     Server -> [pixy,prediction] -> Processing visualisation
      <- [prediction] <-

Sources:
https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data
"""

import json
import struct
import socket

class IPC():
    
    def __init__(self):
        self.soc = socket.socket()

    def __del__(self):
        if self.soc:
            self.soc.close()
        else:
            print("__del__() - no socket to close")

    def close(self):
        if self.soc:
            self.soc.close()
        else:
            print("close() - no socket to close")

    def bind(self, port):
        self.node = "SERVER"
        self.port = port
        print("Binding to " + str(socket.gethostname()) + ":" + str(self.port))
        # bind to address
        self.soc.bind(('192.168.4.3', self.port))
        print("Bound. Listening for connections...")
        # listen for one connection (blocking)
        self.soc.listen(1)
        # accept connection
        self.client_socket, self.addr = self.soc.accept()
        print("Connected")
    
    def hostname(self):
        return socket.gethostname()

    def connect(self, host, port):
        self.node = "CLIENT"
        self.host = host
        self.port = port
        print("Connecting to " + self.host + ":" + str(self.port))
        self.soc.connect((self.host, self.port))
        print("Connected")

    def send(self, obj):
        # json encode
        encoded_message = json.dumps(obj).encode('utf-8')
        # get length of message
        msg_len = len(encoded_message)
        # pack into message where the first 4 bytes is the length
        msg = struct.pack('>I', msg_len) + encoded_message
        # send the message 
        if self.node == "SERVER":
            self.client_socket.sendall(msg)
        if self.node == "CLIENT":
            self.soc.sendall(msg)

    def recv(self):
        # read message length
        raw_msglen = self.recvall(4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data
        raw_msg = self.recvall(msglen)
        if not raw_msg:
            return None
        # decode & return
        return json.loads(raw_msg.decode('utf-8'))

    def recvall(self, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = b''
        while len(data) < n:
            if self.node == "SERVER":
                packet = self.client_socket.recv(n - len(data))
            if self.node == "CLIENT":
                packet = self.soc.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data

#!/usr/bin/env python3
import socket
import time

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 50000      # The port used by the server

class Client:

    def __init__(self,HOST='127.0.0.1',PORT=50000):
        self.host = HOST
        self.port = PORT

    def print_message(self, data):

        print("Data:",  data)

    def connect(self):
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((self.host, self.port))

    def execute(self,   action, value,  sleep_t=0.5):

        self.s.sendall(str.encode(action+" "+value))
        data = self.s.recv(2048)
        print('Received', repr(data))
        msg = data.decode()
        time.sleep(sleep_t)
        return msg

if  __name__=="__main__":

    client = Client('127.0.0.1',    50000)

    res = client.connect()


    res.execute("info", "view")

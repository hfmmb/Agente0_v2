import zmq
import random
import time
from project_commons import *


class Client:

    def __init__(self, ip="127.0.0.1", port=50000):
        context = zmq.Context()
        print("Connecting to server...")
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://" + ip + ":" + str(port))
        #socket.connect("tcp://*:"+str(port))
        self.connected = socket
        pass

    def send_request(self, request_header="info", request="south"):
        """
        Sends a request\command to the server and waits for a reply.

        :param request_header : string -> Contains the descriptor of the request <info; command; ...>
        :param request : string -> Contains the command or message to send to the server <north; east; ...>
        :return: reply -> Contains the reply that the server sent to the client, contents can vary.
        """
        # Sending request to server
        #print("Sending request...")
        # self.connected.send(request_header+" "+ request)
        self.connected.send_string(str(self.send_object_hash()) + " " + request_header + " " + request)
        # Reading the reply from server
        #print("Waiting for reply...")
        reply = self.connected.recv(CONST_NETWORK_STREAM_BYTE_SIZE)
        # Printing the reply
        #print("Reply from server: ", reply)
        time.sleep(0.5)
        return reply

    def send_object_hash(self):
        """
        Returns the hash of the client object as a string.
        :returns Client hash value
        """
        return self.__hash__()


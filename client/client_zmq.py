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
        print("Sending request...")
        # self.connected.send(request_header+" "+ request)
        self.connected.send_string(request_header + " " + request)
        #request = request_header+request
        #self.connected.send_unicode(request_header + " " + request)
        #self.connected.send(request_header,request)
        # Reading the reply from server
        print("Waiting for reply...")
        reply = self.connected.recv(CONST_NETWORK_STREAM_BYTE_SIZE)
        # Printing the reply
        print("Reply from server: ", reply)
        time.sleep(0.05)
        return reply

    def depth_search(self, depth_of_search, list_coordinates_play):
        """
        Recursively calls itself until it reaches the given depth,
        finds a path to the goal or exhausts all possible options.
        Uses an unweighted depth search algorithm as basis.

        @:param depth_of_search : int -> Sets how much steps\plays ahead can the algorithm see in the world.
        @:param list_coordinates_play : list -> Coordinates of mother method to calculate.
        @:returns list_coordinates_play : list -> Coordinates to goal on success, None on failure.
        """
        if depth_of_search > 0:
            depth_of_search -= 1
            while True:
                if len(list_coordinates_play > 0):
                    random_index = random.randrange(0, len(list_coordinates_play))
                    return self.depth_search(depth_of_search, list_coordinates_play)

                else:
                    return None

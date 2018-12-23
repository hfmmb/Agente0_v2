import zmq
from project_commons import *
import random


class Server:

    def __init__(self, ip="127.0.0.1", port=50000):
        context = zmq.Context()
        socket = context.socket(zmq.REP)

        socket.bind("tcp://*:" + str(port))
        self.connected = socket


    def close_connection(self):
        self.connected.close()
        pass

    @staticmethod
    def randomize_buffer(data):
        """
        Recives the data sent by the  clients stored in the buffer, and randomizes the instruction order of said data.
        :param data: List -> Contains the original unrandomized data
        :return: ordered_data -> Contains the final randomized data buffer
        """
        ordered_data = []
        for i in range(len(data)):
            if len(ordered_data) <= 0:
                ordered_data.append(data.pop())
            else:
                ordered_data.insert(random.randrange(0, len(data)), data.pop(random.randrange(0, len(data))))

        return ordered_data

import zmq
from project_commons import *


class Server:

    def __init__(self, ip="127.0.0.1", port=50000):
        context = zmq.Context()
        socket = context.socket(zmq.REP)

        socket.bind("tcp://*:" + str(port))
        #socket.bind("tcp://" + ip + ":" + str(port))
        #socket.bind("tcp://wlp8s0:" + str(port))
        self.connected = socket
        pass

    def close_connection(self):
        pass

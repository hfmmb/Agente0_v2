import time
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

    def new_listener(self):
        while True:
            print("Server online\nListening for requests...")
            message = self.connected.recv(CONST_NETWORK_STREAM_BYTE_SIZE)  # Receives a request from the client
            print("Received request: %s" % message)  # Prints the content of the request

            time.sleep(1)
            #self.connected.send(b"World")
        pass

    def stop_listener(self):
        self.connected.disable_monitor()
        pass

    def close_connection(self):
        pass

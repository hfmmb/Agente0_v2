import time
import zmq


class Server:

    def __init__(self, ip="127.0.0.1", port=50000):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://" + ip + ":" + str(port))
        self.connected = socket
        pass

    def new_connection(self):
        pass

    def new_listener(self):
        while True:
            print("Server online\nListening for requests...")
            message = self.connected.recv()
            print("Received request: %s" % message)

            time.sleep(1)
            self.connected.send(b"World")
        pass

    def stop_listener(self):
        self.connected.disable_monitor()
        pass

    def close_connection(self):
        pass

import zmq


class Client:

    def __init__(self, ip="127.0.0.1", port=50000):
        context = zmq.Context()
        print("Connecting to server...")
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://" +
                       ip +
                       ":" +
                       str(port))
        self.connected = socket
        pass

    def send_message(self,request=None):
        #Sending request to server
        print("Sending request...")
        self.connected.send(b"Hello")
        #Reading the reply from server
        print("Waiting for reply...")
        reply = self.connected.recv()
        #Printing the reply
        print("Reply: ", reply)

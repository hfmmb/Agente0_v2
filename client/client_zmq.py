import zmq
import random


class Client:

    def __init__(self, ip="83.132.205.201", port=50000):
        context = zmq.Context()
        print("Connecting to server...")
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://" + ip + ":" + str(port))
        self.connected = socket
        pass

    def send_request(self, request=None):
        # Sending request to server
        print("Sending request...")
        self.connected.send(b"Hello")
        # Reading the reply from server
        print("Waiting for reply...")
        reply = self.connected.recv()
        # Printing the reply
        print("Reply: ", reply)


    def pesquisa_profundidade(self, depth_of_search, lista_coordenadas_jogada):
        """
        Recursively calls itself until it reaches the given depth,
        finds a path to the goal or exhausts all possible options.
        Uses an unweighted depth search algorithm as basis.

        @:parameter depth_of_search : int -> Sets how much steps\plays ahead can the algorithm see in the world.
        @:parameter lista_lista_coordenadas_jogada : list -> Coordinates of mother method to calculate.
        @:returns lista_coordenadas_jogada : list -> Coordinates to goal on success, None on failure.
        """
        if depth_of_search > 0:
            depth_of_search -= 1
            while True:
                if len(lista_coordenadas_jogada > 0):
                    random_index = random.randrange(0, len(lista_coordenadas_jogada))
                    return self.pesquisa_profundidade(depth_of_search, lista_coordenadas_jogada)

                else:
                    return None

import zmq
import random


class Client:

    def __init__(self, ip="127.0.0.1", port=50000):
        context = zmq.Context()
        print("Connecting to server...")
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://" + ip + ":" + str(port))
        self.connected = socket
        pass

    def send_request(self,request_header="info", request=None):
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
        # Reading the reply from server
        print("Waiting for reply...")
        reply = self.connected.recv(2048)
        # Printing the reply
        print("Reply: ", reply)
        return reply

    def pesquisa_profundidade(self, depth_of_search, lista_coordenadas_jogada):
        """
        Recursively calls itself until it reaches the given depth,
        finds a path to the goal or exhausts all possible options.
        Uses an unweighted depth search algorithm as basis.

        @:param depth_of_search : int -> Sets how much steps\plays ahead can the algorithm see in the world.
        @:param lista_lista_coordenadas_jogada : list -> Coordinates of mother method to calculate.
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

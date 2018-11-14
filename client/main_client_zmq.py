"""
@autores: Hélder Filipe M. de M. Braga <helderbraga.work@gmail.com>;
          João Pedro Moreira Sousa <joao.sousa201@gmail.com>;
          Leandro Jorge O. Branco;

@since: 12/11/2018

Creates a client server connection to send and receive commands with the help of the module ZeroMQ <pyzmq>, this method
makes the connection more reliable and stable than doing it directly using sockets. This is the Client side of the
Client-Server network arquiteture.

ZeroMQ: http://zguide.zeromq.org/
"""

from client_zmq import Client
import ast
import random
from tkinter import messagebox


c = Client()
c.send_request()
#path_to_goal = [c.send_request("info", "position"),  # Current Position
#                c.send_request("info", "north"),     # Up
#                c.send_request("info", "south"),     # Down
#                c.send_request("info", "west"),      # Left
#                c.send_request("info", "east")]      # Right

#If   [list of coordenates to goal] then the goal was found
#Else [None] then the goal was not found
#path_to_goal = c.pesquisa_profundidade(5, path_to_goal)

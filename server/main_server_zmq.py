"""
@autores: Hélder Filipe M. de M. Braga <helderbraga.work@gmail.com>;
          João Pedro Moreira Sousa <joao.sousa201@gmail.com>;
          Leandro Jorge O. Branco;

@since: 12/11/2018

Creates a client server connection to send and receive commands with the help of the module ZeroMQ <pyzmq>, this method
makes the connection more reliable and stable than doing it directly using sockets. This is the Server side of the
Client-Server network arquiteture.

ZeroMQ: http://zguide.zeromq.org/
"""

from server import game_board
from server.server_zmq import Server
from server import game_board
import sys
import random
import tkinter
import time
import traceback

s = Server()
s.new_listener()

"""
@authors: Hélder Filipe M. de M. Braga <helderbraga.work@gmail.com>;
          João Pedro Moreira Sousa <joao.sousa201@gmail.com>;
          Leandro Jorge O. Branco <branco.leandro23@gmail.com>;

@since: 12/11/2018

Creates a client server connection to send and receive commands with the help of the module ZeroMQ <pyzmq>, this method
makes the connection more reliable aand stable than doing it directly using sockets. This is the Server side of the
Client-Server network architecture.

ZeroMQ: http://zguide.zeromq.org/
"""

from server.server_zmq import Server
from server import game_board as gb
import random
import tkinter as tk
from server.__init__ import *
from project_commons import *
import time
import sys
import zmq
import threading

s = Server()


def initialize_obstacles(image_dir, list_obstacles):
    i = 1
    for obstacle in list_obstacles:

        ob = gb.Obstacle(image_dir, 'ob' + str(i), obstacle[0], obstacle[1], 'obstacle' + str(i), False)
        board.add(ob, obstacle[0], obstacle[1])
        i += 1


def initialize_goal(dir_image, pos):

    goal = gb.Goal(dir_image, 'goal1', pos[0], pos[1], 'goal', False)
    board.add(goal, pos[0], pos[1])


def initialize_bomb(dir_image, list_bombs, rows, columns):
    i = 1
    for b in list_bombs:
        bomb = gb.Bomb(dir_image, 'bomb' + str(i), b[0], b[1])
        board.add(bomb, b[0], b[1])
        if b[0] >= rows - 1:
            new_b = 0
        else:
            new_b = b[0]+1
        bomb_s = gb.BombSound(dir_image, 'bomb_sound_s' + str(i), new_b, b[1])
        board.add(bomb_s, new_b, b[1])
        if b[1] >= columns - 1:
            new_b = 0
        else:
            new_b = b[1]+1
        bomb_s = gb.BombSound(dir_image, 'bomb_sound_e' + str(i), b[0], new_b)
        board.add(bomb_s, b[0], new_b)
        if b[0] <= 0:
            new_b = columns - 1
        else:
            new_b = b[0]-1
        bomb_s = gb.BombSound(dir_image, 'bomb_sound_n' + str(i), new_b, b[1])
        board.add(bomb_s, new_b, b[1])
        if b[1] <= 0:
            new_b = rows - 1
        else:
            new_b = b[1]-1

        bomb_s = gb.BombSound(dir_image, 'bomb_sound_w' + str(i), b[0], new_b)
        board.add(bomb_s, b[0], new_b)
        i = i + 1


def initialize_weights(image_dir):
    patch = [[0 for x in range(CONST_BOARD_COLUMNS)] for x in range(CONST_BOARD_ROWS)]
    weight = 1.0
    name = ''
    for column in range(0, 16):
        for row in range(0, 16):
            res = random.uniform(0, 1.0)
            if res <= 0.3:
                name = "patch_clear"
                weight = 1.0
            elif res <= 0.5:
                weight = 1.1  # 2.0
                name = "patch_lighter"
            elif res <= 0.7:
                weight = 1.2  # 4.0
                name = "patch_middle"
            elif res <= 1.0:
                weight = 1.3  # 8.0
                name = "patch_heavy"
            patch[column][row] = gb.Patch(image_dir, 'patch' + str(column) + "-" + str(row),
                                          name, column, row, weight, False)
            board.add(patch[column][row], column, row)

#def data_buffer(buffer):
#    while True:
#        if timer.is_alive():
#            data = s.connected.recv(CONST_NETWORK_STREAM_BYTE_SIZE)
#            local_hash, header, value = data.decode().split()
#            if local_hash not in buffer:
#                buffer[local_hash] = header, value
#                print(buffer)
#        else:
#            timer.cancel()
#            return buffer
def verify_winner(agent):
    x_player = agent.get_x()
    y_player = agent.get_y()
    x_goal, y_goal = board.getgoalposition(agent)
    if x_player == x_goal and y_player == y_goal:
        msg = "  O " + str(agent.get_name()) + " venceu o jogo"
        broadcast_loop(str(msg))


def loop():

            print("Listening...")
#            buffer = {}
#            timer = threading.Timer(BUFFER_TIME_INTERVAL, data_buffer)
#            timer.start()



            while True:
                    try:
                        data = s.connected.recv(CONST_NETWORK_STREAM_BYTE_SIZE)
                        local_hash, header, value = data.decode().split()
                        if local_hash not in AGENTS_DICT:
                            new_player(local_hash)

                    except ValueError as erro_excepcao:
                        print("Valor nulo ou menor que dois?", erro_excepcao)
                        break
                    try:
                        agent = AGENTS_DICT.get(local_hash)
                    except KeyError as erro_excepcao:
                        print("Chave  não encontrada",erro_excepcao)
                    res = ''
                    if header == 'command':
                        # -----------------------
                        # movements without considering the direction
                        # of the face of the object but testing the objects
                        # -----------------------
                        if value == 'north':
                            agent.close_eyes()
                            res = board.move_north(agent, 'forward')
                            if not board.is_target_obstacle(res):
                                board.change_position(agent, res[0], res[1])
                            msg = "  O " + str(agent.get_name()) + " deslocou-se para as coordenadas(" + str(agent.get_x()) + "," + str(agent.get_y()) + ")"
                            broadcast_loop(str(msg))


                        elif value == 'south':
                            agent.close_eyes()
                            res = board.move_south(agent, 'forward')
                            if not board.is_target_obstacle(res):
                                board.change_position(agent, res[0], res[1])
                            msg = "  O " + str(agent.get_name()) + " deslocou-se para as coordenadas(" + str(agent.get_x()) + "," + str(agent.get_y()) + ")"
                            broadcast_loop(str(msg))

                        elif value == 'east':

                            agent.close_eyes()
                            res = board.move_east(agent, 'forward')
                            if not board.is_target_obstacle(res):
                                board.change_position(agent, res[0], res[1])
                            msg = "  O " + str(agent.get_name()) + " deslocou-se para as coordenadas(" + str(agent.get_x()) + "," + str(agent.get_y()) + ")"
                            broadcast_loop(str(msg))

                        elif value == 'west':
                            agent.close_eyes()
                            res = board.move_west(agent, 'forward')
                            if not board.is_target_obstacle(res):
                                board.change_position(agent, res[0], res[1])
                            msg = "  O " + str(agent.get_name()) + " deslocou-se para as coordenadas(" + str(agent.get_x()) + "," + str(agent.get_y()) + ")"
                            broadcast_loop(str(msg))


                        # -----------------------
                        # move to home
                        # -----------------------
                        elif value == 'home':
                            res = board.move_home(agent)

                        elif value == 'forward':
                            res = board.move(agent, 'forward')

                        elif value == 'left':
                            res = board.turn_left(agent)

                        elif value == 'right':
                            res = board.turn_right(agent)

                        elif value == "set_steps":
                            res = board.set_stepsview(agent)

                        elif value == "reset_steps":
                            res = board.reset_stepsview(agent)

                        elif value == "open_eyes":
                            res = agent.open_eyes()

                        elif value == "close_eyes":
                            res = agent.close_eyes()
                        elif value == "clean_board":
                            res = board.clean_board()
                        elif value == "bye" or value == "exit":
                            exit(1)
                        else:
                            pass
                        verify_winner(agent)
                    elif header == 'info':
                        if value == 'direction':
                            res = agent.get_direction()
                        elif value == 'view':
                            front = board.getplaceahead(agent)
                            res = board.view_object(agent, front)
                        elif value == "weights":
                            res = board.view_weights(agent, 'front')
                        elif value == 'map':
                            print('Map:', board.view_global_weights(agent))
                            res = board.view_global_weights(agent)
                        elif value == 'obstacles':
                            print('Obstacles:', board.view_obstacles(agent))
                            res = board.view_obstacles(agent)
                        elif value == 'goal' or value == 'target':
                            res = board.getgoalposition(agent)
                        elif value == 'position':
                            res = (agent.get_x(), agent.get_y())
                        elif value == 'maxcoord':
                            res = board.get_maxcoord()
                        elif value == 'north':
                            # View north
                            front = board.getplacedir(agent, 'north')
                            res = board.view_object(agent, front)
                            print("NORTH: ", res)
                        elif value == 'south':
                            # View north
                            front = board.getplacedir(agent, 'south')
                            res = board.view_object(agent, front)
                            print("SOUTH: ", res)
                        elif value == 'east':
                            # View north
                            front = board.getplacedir(agent, 'east')
                            res = board.view_object(agent, front)
                            print("EAST: ", res)

                        elif value == 'west':
                            # View north
                            front = board.getplacedir(agent, 'west')
                            res = board.view_object(agent, front)
                            print("WEST: ", res)

                        else:
                            pass
                    if res != '':
                        return_data = str.encode(str(res))
                    else:
                        return_data = str.encode(
                            "what? "
                            "commands = <forward, left, right, set_steps, reset_steps, open_eyes, close_eyes>"
                            "info = <direction, view, weights, map, goal, position, obstacles, maxcoord>")
                    s.connected.send(return_data)
                    root.update()

def broadcast_loop(msg = "Connected"):
    context = zmq.Context()

    sock = context.socket(zmq.PUB)
    sock.bind("tcp://*:5000")

    x = 0
    while x < 3:
        time.sleep(1)
        sock.send_string(msg)
        x = x + 1





player_coordinates = [CONST_PLAYER_COORD_X, CONST_PLAYER_COORD_Y]

def new_player(hash):
    global player_coordinates
    global AGENT_COUNT
    x = 0
    y = 0
    if AGENT_COUNT > 0:
        for i in AGENTS_DICT:
            comparacao = AGENTS_DICT[i].get_home()

            if x == comparacao[0] and y == comparacao[1]:
                player_coordinates = [1, 2]




    # Initialize player
    agent = gb.Player(CONST_IMAGE_DIR, 'player' + str(AGENT_COUNT), player_coordinates[0], player_coordinates[1], 'south', 'front', True)
    agent.set_home((player_coordinates[0], player_coordinates[1]))
    agent.close_eyes()

    # Add player
    board.add(agent, player_coordinates[0], player_coordinates[1])
    root.update()
    AGENT_COUNT += 1

    AGENTS_DICT[hash] = agent #Dicionario que guarda os agentes



if __name__ == "__main__":

    print("Starting the Game Board")

    root = tk.Tk()
    board = gb.GameBoard(root, CONST_BOARD_ROWS, CONST_BOARD_COLUMNS)
    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    # BOARD BOARD:
    initialize_obstacles(CONST_IMAGE_DIR, [])
    initialize_goal(CONST_IMAGE_DIR, (CONST_GOAL_COORD_X, CONST_GOAL_COORD_Y))
    initialize_bomb(CONST_IMAGE_DIR, [], CONST_BOARD_ROWS, CONST_BOARD_COLUMNS)
    root.update()
    # Loop
    loop()


"""
@authors: Hélder Filipe M. de M. Braga <helderbraga.work@gmail.com>;
          João Pedro Moreira Sousa <joao.sousa201@gmail.com>;
          Leandro Jorge O. Branco <branco.leandro23@gmail.com>;

@since: 12/11/2018

Creates a client server connection to send and receive commands with the help of the module ZeroMQ <pyzmq>, this method
makes the connection more reliable and stable than doing it directly using sockets. This is the Server side of the
Client-Server network architecture.

ZeroMQ: http://zguide.zeromq.org/
"""

from server.server_zmq import Server
from server import game_board as gb
import random
import tkinter as tk
from server.__init__ import *
from project_commons import *

s = Server()


def initialize_obstacles(image_dir, list_obstacles):
    i = 1
    for obstacle in list_obstacles:

        ob = gb.Obstacle(image_dir, 'ob' + str(i), obstacle[0], obstacle[1], 'obstacle' + str(i), False)
        board.add(ob, obstacle[0], obstacle[1])
        i += 1

    # ob1 = gb.Obstacle('ob1', 0, 3, 'obstacle1', False)
    # board.add(ob1, 0, 3)
    # ob2 = gb.Obstacle('ob2', 3, 4, 'obstacle1', False)
    # board.add(ob2,3, 4)
    # ob3 = gb.Obstacle('ob3', 2, 2, 'obstacle1', False)
    # board.add(ob3, 2, 2)
    # ob4 = gb.Obstacle('ob4', 5, 3, 'obstacle1', False)
    # board.add(ob4, 5, 3)
    # ob5 = gb.Obstacle('ob5', 1, 5, 'obstacle1', False)
    # board.add(ob5, 1, 5)
    # ob6 = gb.Obstacle('ob6', 6, 6, 'obstacle1', False)
    # board.add(ob6, 6, 6)


def initialize_goal(dir_image, pos):
    #    goal = gb.Goal('goal1', 10, 12, 'goal', False)
    #    board.add(goal, 10, 12)
    goal = gb.Goal(dir_image, 'goal1', pos[0], pos[1], 'goal', False)
    board.add(goal, pos[0], pos[1])
    # print(pos[0],pos[1])


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
            # print(res)
            board.add(patch[column][row], column, row)


def loop():

            print("Listening...")
            while True:
                    try:
                        data = s.connected.recv(CONST_NETWORK_STREAM_BYTE_SIZE)
                        header, value = data.decode().split()
                        print("Header: ",header,"Value:", value)

                    except ValueError as erro_excepcao:
                        print("Valor nulo ou menor que dois?", erro_excepcao)
                        break
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

                        elif value == 'south':
                            agent.close_eyes()
                            res = board.move_south(agent, 'forward')
                            if not board.is_target_obstacle(res):
                                board.change_position(agent, res[0], res[1])

                        elif value == 'east':
                            agent.close_eyes()
                            res = board.move_east(agent, 'forward')
                            if not board.is_target_obstacle(res):
                                board.change_position(agent, res[0], res[1])

                        elif value == 'west':
                            agent.close_eyes()
                            res = board.move_west(agent, 'forward')
                            if not board.is_target_obstacle(res):
                                board.change_position(agent, res[0], res[1])

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
                            # print('Goal:',res)
                        elif value == 'position':
                            res = (agent.get_x(), agent.get_y())
                            # print('Position:', res)
                        elif value == 'maxcoord':
                            res = board.get_maxcoord()
                            # print('MaxCoordinates:', res)
                        elif value == 'north':
                            # View north
                            front = board.getplacedir(agent, 'north')
                            print("Front: ", front, res)
                            res = board.view_object(agent, front)
                            print("Front after:",front)
                            print("NORTH: ", res)
                            #res = front
                        elif value == 'south':
                            # View north
                            front = board.getplacedir(agent, 'south')
                            res = board.view_object(agent, front)
                            print("SOUTH: ", res)
                            print("Front after:", front)
                            #res = front
                        elif value == 'east':
                            # View north
                            front = board.getplacedir(agent, 'east')
                            res = board.view_object(agent, front)
                            print("EAST: ", res)

                            print("Front after:", front)
                            #res = front
                        elif value == 'west':
                            # View north
                            front = board.getplacedir(agent, 'west')
                            res = board.view_object(agent, front)
                            print("WEST: ", res)

                            print("Front after:",front)
                            #res = front
                        else:
                            pass
                    if res != '':
                        print("Res: ",res)
                        return_data = str.encode(str(res))
                        print("data: ", return_data)
                    else:
                        return_data = str.encode(
                            "what? "
                            "commands = <forward, left, right, set_steps, reset_steps, open_eyes, close_eyes>"
                            "info = <direction, view, weights, map, goal, position, obstacles, maxcoord>")
                    s.connected.send(return_data)
                    root.update()


player_coordinates = [CONST_PLAYER_COORD_X, CONST_PLAYER_COORD_Y]
if __name__ == "__main__":

    print("Starting the Game Board")

    root = tk.Tk()
    board = gb.GameBoard(root, CONST_BOARD_ROWS, CONST_BOARD_COLUMNS)
    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    # BOARD BOARD:
    initialize_obstacles(CONST_IMAGE_DIR, [])
    initialize_goal(CONST_IMAGE_DIR, (CONST_GOAL_COORD_X, CONST_GOAL_COORD_Y))
    initialize_bomb(CONST_IMAGE_DIR, [], CONST_BOARD_ROWS, CONST_BOARD_COLUMNS)
    # initialize_weights(CONST_IMAGE_DIR)
    root.update()
    # PLAYER PLAYER:
    # Initialize player
    agent = gb.Player(CONST_IMAGE_DIR, 'player', player_coordinates[0], player_coordinates[1], 'south', 'front', True)
    agent.set_home((player_coordinates[0], player_coordinates[1]))
    agent.close_eyes()
    # Add player
    board.add(agent, player_coordinates[0], player_coordinates[1])
    root.update()

    # Loop
    loop()

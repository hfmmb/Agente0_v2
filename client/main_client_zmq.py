"""
@autores: Hélder Filipe M. de M. Braga <helderbraga.work@gmail.com>;
          João Pedro Moreira Sousa <joao.sousa201@gmail.com>;
          Leandro Jorge O. Branco <branco.leandro23@gmail.com>;

@since: 12/11/2018

Creates a client server connection to send and receive commands with the help of the module ZeroMQ <pyzmq>, this method
makes the connection more reliable and stable than doing it directly using sockets. This is the Client side of the
Client-Server network arquiteture.

ZeroMQ: http://zguide.zeromq.org/
"""

from client.client_zmq import Client
import random
from tkinter import messagebox
from server.__init__ import *
import threading
import time
import zmq
import ast
import sys
aux = ''
c = Client()

# path_to_goal = [c.send_request("info", "position"),  # Current Position
#                c.send_request("info", "north"),     # Up
#                c.send_request("info", "south"),     # Down
#                c.send_request("info", "west"),      # Left
#                c.send_request("info", "east")]      # Right

# If   [list of coordenates to goal] then the goal was found
# Else [None] then the goal was not found
# path_to_goal = c.pesquisa_profundidade(5, path_to_goal)


def trepa_colinas():

        contador_tentativas = 0
        goal_raw = c.send_request("info", "goal")
        coord_x = goal_raw.decode()  # Getting the numbers only
        coord_y = coord_x[4]  # Store coordinate y
        coord_x = coord_x[1]  # Store coordinate x
        goal = [int(coord_x), int(coord_y)]  # Store in goal after conversion to integer

        startting_position_raw = c.send_request("info", "position")
        coord_x = startting_position_raw.decode()
        coord_y = coord_x[4]  # Store coordinate y
        coord_x = coord_x[1]  # Store coordinate x
        starting_position = [int(coord_x), int(coord_y)]
        c.send_request("raio", str(1))

        while not(starting_position[0] == goal[0] and starting_position[1] == goal[1]):

            try: #NORTH, soutH,east,west
                possibility_list = []

                raw = c.send_request("info", "north")
                north = raw.decode()
                raw = c.send_request("info", "south")
                south = raw.decode()
                raw = c.send_request("info", "east")
                east = raw.decode()
                raw = c.send_request("info", "west")
                west = raw.decode()

                possibility_list = [north[0], south[0], east[0], west[0]]  # List of the possibilities in the current position


                generated_random_number = random.randint(0, 1)
                if generated_random_number == 0:
                    if starting_position[0] != goal[0]:
                        if starting_position[0] > goal[0]:
                            if possibility_list[2] == ("['obstacle']"):
                                print("Obstáculo à frente")
                                contador_tentativas += 1
                                if contador_tentativas > 3:
                                    rand = random.randint(0, 2)
                                    if rand == 0:
                                        if possibility_list[3] != ("['obstacle']") and possibility_list[3] != ("['player']") and \
                                                starting_position[0] < (CONST_BOARD_ROWS-1):

                                            starting_position[0] += 1
                                            c.send_request("command", "east")

                                    elif rand == 1:
                                        if possibility_list[0] != ("['obstacle']") and possibility_list[0] != ("['player']") and starting_position[1] > 0:
                                            starting_position[1] -= 1
                                            c.send_request("command", "north")

                                    elif rand == 2:
                                        if possibility_list[1] != ("['obstacle']") and possibility_list[1] != ("['player']") and \
                                                starting_position[1] < (CONST_BOARD_ROWS-1):

                                            starting_position[1] += 1
                                            c.send_request("command", "south")

                                    contador_tentativas = 0
                            elif possibility_list[3] == ("['bomb']"):
                                print("Bomba à frente")
                            elif possibility_list[2] == ("['player']"):
                                print("Bomba à frente")
                            else:
                                c.send_request("command", "west")
                                starting_position[0] -= 1

                        if starting_position[0] < goal[0]:
                            if possibility_list[3] == ("['obstacle']"):
                                print("Obstaculo à frente")
                                contador_tentativas += 1
                                if contador_tentativas > 3:
                                    rand = random.randint(0, 2)
                                    if rand == 0:
                                        if possibility_list[2] != ("['obstacle']") and possibility_list[2] != ("['player']") and starting_position[0] > 0:
                                            starting_position[0] -= 1
                                            c.send_request("command", "west")

                                    elif rand == 1:
                                        if possibility_list[0] != ("['obstacle']") and possibility_list[0] != ("['player']") and starting_position[1] > 0:
                                            starting_position[1] -= 1
                                            c.send_request("command", "north")

                                    elif rand == 2:
                                        if possibility_list[1] != ("['obstacle']") and possibility_list[1] != ("['player']")  and \
                                                starting_position[1] < (CONST_BOARD_ROWS-1):
                                            starting_position[1] += 1
                                            c.send_request("command", "south")

                                    contador_tentativas = 0
                            elif possibility_list[2] == ("['bomb']"):
                                print("Bomba à frente")
                            elif possibility_list[2] == ("['player']"):
                                print("Player á frente")
                            else:
                                c.send_request("command", "east")
                                starting_position[0] += 1
                elif generated_random_number == 1:
                    if starting_position[1] != goal[1]:
                        if starting_position[1] > goal[1]:
                            if possibility_list[0] == ("['obstacle']"):
                                print("obstaculo a frente")
                                contador_tentativas += 1
                                if contador_tentativas > 3:
                                    rand = random.randint(0, 2)
                                    if rand == 0:
                                        if possibility_list[2] != "['obstacle']" and possibility_list[2] != "['player']" and starting_position[0] > 0:
                                            starting_position[0] -= 1
                                            c.send_request("command", "west")

                                    elif rand == 1:
                                        if possibility_list[3] != "['obstacle']" and possibility_list[3] != "['player']" and \
                                                starting_position[0] < (CONST_BOARD_COLUMNS-1):
                                            starting_position[0] += 1
                                            c.send_request("command", "east")

                                    elif rand == 2:
                                        if possibility_list[1] != "['obstacle']" and possibility_list[1] != "['player']" and \
                                                starting_position[1] < (CONST_BOARD_COLUMNS-1):
                                            starting_position[1] += 1
                                            c.send_request("command", "south")

                                    contador_tentativas = 0
                            elif possibility_list[0] == "['bomb']":
                                print("bomba a frente")

                            elif possibility_list[0] == "['player']":
                                print("Player á frente")
                            else:
                                c.send_request("command", "north")
                                starting_position[1] -= 1

                        if starting_position[1] < goal[1]:
                            if possibility_list[1] == "['obstacle']":
                                print("obstaculo a frente")
                                contador_tentativas += 1
                                if contador_tentativas > 3:
                                    rand = random.randint(0, 2)
                                    if rand == 0:
                                        if possibility_list[2] != ("['obstacle']") and possibility_list[2] != ("['player']") and starting_position[0] > 0:
                                            starting_position[0] -= 1
                                            c.send_request("command", "west")

                                    elif rand == 1:
                                        if possibility_list[3] != ("['obstacle']") and possibility_list[3] != ("['player']") and \
                                                starting_position[0] < (CONST_BOARD_COLUMNS-1):

                                            starting_position[0] += 1
                                            c.send_request("command", "east")

                                    elif rand == 2:
                                        if possibility_list[0] != ("['obstacle']") and possibility_list[0] != ("['player']") and starting_position[1] > 0:
                                            starting_position[1] -= 1
                                            c.send_request("command", "north")

                                    contador_tentativas = 0
                            elif possibility_list[1] == ("['bomb']"):
                                print("bomba a frente")
                            elif possibility_list[1] == ("['player']"):
                                print("Player a frente")
                            else:
                                c.send_request("command", "south")
                                starting_position[1] += 1

            except ConnectionError as excepcao_erro:
                print("Server ligado?", excepcao_erro)

        messagebox.showinfo("Vitoria", "Goal Achieved")

        exit()


def depth_search(depth_of_search, road_list, position, goal):
    """
    Recursively calls itself until it reaches the given depth,
    finds a path to the goal or exhausts all possible options.
    Uses an unweighted depth search algorithm as basis.

    @:param depth_of_search : int -> Sets how much steps\plays ahead can the algorithm see in the world.
    @:param road_list : list -> Coordinates of mother method to calculate.
    @:param position : int -> Current coordinates of the algorythm
    @:param goal : int -> Coordinates of the goal
    @:returns road_list : list -> Coordinates to goal on success, None on failure.
    """
    if position == goal:  # Checks if it has reached the goal
        return road_list
    if depth_of_search > 0:
            depth_of_search -= 1 # Decreases the deph

            raw = c.send_request("info", "south")
            south = raw.decode()
            real_south = ast.literal_eval(south)
            raw =  c.send_request("info", "east")
            east = raw.decode()
            real_east = ast.literal_eval(east)
            raw = c.send_request("info", "north")
            north = raw.decode()
            real_north = ast.literal_eval(north)
            raw = c.send_request("info", "west")
            west = raw.decode()
            real_west = ast.literal_eval(west)

            possibility_list = [str(real_south[0]), str(real_east[0]), str(real_north[0]), str(real_west[0])] # List of the possibilities in the current position

            contador = 0
            prev_posi = [] #auxiliar variable
            while contador <= 3: # cycle to go through all 4 possibilities.. Each number is a possibility 0 == south | 1 == east | 2 == north | 3 == West

                if possibility_list[contador] == "[]" or possibility_list[contador] == "['goal']": # checks if the current possibility is empty or goal
                    if contador == 0 and position[1] < 5:  # if "contador" == 0 then he is going to try to go south
                        c.send_request("command", "south")
                        prev_posi = position
                        position = [position[0], position[1] + 1]
                        road_list.append(position)

                        check = depth_search(depth_of_search, road_list, position, goal) #calls the function again with the new values

                        if check == "no deph" or check == "no possibilities":  # if the goal wasnt found then the variables return to their previous values
                            position = prev_posi
                            c.send_request("command", "north")
                            road_list.pop()
                        else: # if "check" was different from "no deph" and "no possibilities" then that means it found the GOAL
                            return check

                    elif contador == 1 and position[0] < 5: #Same thing that was done above  but for the EAST
                        c.send_request("command", "east")
                        prev_posi = position
                        position = [position[0] + 1, position[1]]
                        road_list.append(position)
                        check = depth_search(depth_of_search, road_list, position, goal)
                        if check == "no deph" or check == "no possibilities":
                            position = prev_posi
                            c.send_request("command", "west")
                            road_list.pop()
                        else:
                            return check

                    elif contador == 2 and position [1] > 0: #Same thing that was done above  but for the NORTH
                        c.send_request("command", "north")
                        prev_posi = position
                        position = [position[0], position[1] - 1]
                        road_list.append(position)
                        check = depth_search(depth_of_search, road_list, position, goal)
                        if check == "no deph" or check == "no possibilities":
                            position = prev_posi
                            c.send_request("command", "south")
                            road_list.pop()
                        else:
                            return check

                    elif contador == 3 and position[0] > 0: #Same thing that was done above  but for the WEST
                        c.send_request("command", "west")
                        prev_posi = position
                        position = [position[0] -1 , position[1]]
                        road_list.append(position)
                        check = depth_search(depth_of_search, road_list, position, goal)
                        if check == "no deph" or check == "no possibilities":
                            position = prev_posi
                            c.send_request("command", "east")
                            road_list.pop()
                        else:
                            return check




                contador = contador + 1
            return "no possibilities" #It returns this if it finds no possibilities
    else:
        return "no deph" #It returns this if it there is no more deph

def follow_road(list): #Function to make the agent follow the right path
    c.send_request("command", "home") # send the agent back HOME

    raw = c.send_request("info", "position")
    raw_dec = raw.decode()
    position = [int(raw_dec[1]), int(raw_dec[4])] #Current position coordinates

    contador = 0
    while contador < len(list): # cycle to go through all the elements of the list

        c.send_request("info", "position") #


        if position[0] < list[contador][0]: #compare the current X coordinate with the X coordinate of the current element on the list
            position[0] = position[0] + 1 #and change if needed
            c.send_request("command", "east")

        if position[0] > list[contador][0]:
            position[0] = position[0] - 1
            c.send_request("command", "west")

        if position[1] < list[contador][1]:
            position[1] = position[1] + 1
            c.send_request("command", "south")

        if position[1] > list[contador][1]:
            position[1] = position[1] - 1
            c.send_request("command", "north")

        contador = contador + 1

def manual_movement():
    raio = int(input("Digite o valor do raio de visao do agente: "))
    c.send_request("raio", str(raio))
    while True:
        time.sleep(0.2)
        action, value = input("Insert action value pairs:").split()
        print("Action Value pair:", action, ":", value)
        if action == "info":

            raw = c.send_request("info", "position")
            raw_dec = raw.decode()

            if value == "position":

                position = [int(raw_dec[1]), int(raw_dec[4])]
                print("A sua posição: ", position)

            elif value == "north":

                raw_values =c.send_request(action, value)
                x = raw_values.decode()
                real_x = ast.literal_eval(x)
                for i in range(0 , len(real_x)):
                    coord_x = int(raw_dec[1])
                    coord_y = int(raw_dec[4]) - i -1
                    if coord_x >=0 and coord_y >= 0 and coord_x <= 5 and coord_y <= 5:
                        print("Coordinates(", str(coord_x) + "," + str(coord_y), "): ", real_x[i])
            elif value == "south":
                raw_values = c.send_request(action, value)
                x = raw_values.decode()
                real_x = ast.literal_eval(x)
                for i in range(0, len(real_x)):
                    coord_x = int(raw_dec[1])
                    coord_y = int(raw_dec[4]) + i + 1
                    if coord_x >=0 and coord_y >= 0 and coord_x <= 5 and coord_y <= 5:
                        print("Coordinates(", str(coord_x) + "," + str(coord_y), "): ", real_x[i])
            elif value == "east":
                raw_values = c.send_request(action, value)
                x = raw_values.decode()
                real_x = ast.literal_eval(x)
                for i in range(0, len(real_x)):
                    coord_x = int(raw_dec[1]) + i + 1
                    coord_y = int(raw_dec[4])
                    if coord_x >=0 and coord_y >= 0 and coord_x <= 5 and coord_y <= 5:
                        print("Coordinates(", str(coord_x) + "," + str(coord_y), "): ", real_x[i])
            elif value == "west":
                raw_values = c.send_request(action, value)
                x = raw_values.decode()
                real_x = ast.literal_eval(x)
                for i in range(0, len(real_x)):
                    coord_x = int(raw_dec[1]) -i - 1
                    coord_y = int(raw_dec[4])
                    if coord_x >=0 and coord_y >= 0 and coord_x <= 5 and coord_y <= 5:
                        print("Coordinates(", str(coord_x) + "," + str(coord_y), "): ", real_x[i])

            else:

                raw = c.send_request(action, value)
                raw_info = raw.decode()
                print(raw_info)

        elif action == "command" and value == "north" or value == "south" or value == "east" or value == "west":
            raw_x = c.send_request("info", value)
            x = raw_x.decode()
            real_x = ast.literal_eval(x)
            if str(real_x[0]) != ("['player']") and str(real_x[0]) != ("['obstacle']"):
                c.send_request(action, value)
        else:
            c.send_request(action, value)

        raw = c.send_request("info", "position")
        raw_dec = raw.decode()
        position = [int(raw_dec[1]), int(raw_dec[4])]

        raw = c.send_request("info", "goal")
        raw_dec = raw.decode()
        goal = [int(raw_dec[1]), int(raw_dec[4])]

        if position == goal:
            messagebox.showinfo("Vitoria", "Goal Achieved")


def recv_loop():
    global aux
    context = zmq.Context()
    sock = context.socket(zmq.SUB)
    sock.setsockopt_string(zmq.SUBSCRIBE, '')
    arg = "tcp://localhost:5000"
    sock.connect(arg)

    while True:
        time.sleep(0.2)
        message = sock.recv()
        if message != aux:
            print("\n ", message)
            aux = message



x = -1000
while x != 0:

    try:
        x = int(input("Digite: \n (1) - Pesquisa em profundidade \n (2) - Trepa Colinas\n (3) - Manual Movement\n"
                      "Input: "))
        if x == 1:

            c.send_request("raio", str(1))
            deph = int(input(("Digite o valor da profundidade: ")))

            raw = c.send_request("info", "position")
            raw_dec = raw.decode()
            position = [int(raw_dec[1]), int(raw_dec[4])] #current position coordinates in integer

            raw = c.send_request("info", "goal")
            raw_dec = raw.decode()
            goal = [int(raw_dec[1]), int(raw_dec[4])]  #current GOAL coordinates in integer

            road_list = [position] #List that is going to hold the way to the goal
            road_list = depth_search(deph, road_list, position, goal) # this function will get the values for the list
            print(road_list) # prints the list
            follow_road(road_list) #Follows the path to the goal
        elif x == 2:
            trepa_colinas()

        elif x == 3:

            t1 = threading.Thread(target=recv_loop)
            t2 = threading.Thread(target=manual_movement)
            t1.start()
            t2.start()
            t1.join()
            t2.join()
        else:
            print("Valor inexitente ou errado!")
    except ValueError as excepcao_erro:
        print("Valor inexitente ou errado!", excepcao_erro)
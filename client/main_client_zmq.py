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

from client_zmq import Client
import ast
import random
from tkinter import messagebox
import time
from server.__init__ import *

c = Client()

# path_to_goal = [c.send_request("info", "position"),  # Current Position
#                c.send_request("info", "north"),     # Up
#                c.send_request("info", "south"),     # Down
#                c.send_request("info", "west"),      # Left
#                c.send_request("info", "east")]      # Right

# If   [list of coordenates to goal] then the goal was found
# Else [None] then the goal was not found
# path_to_goal = c.pesquisa_profundidade(5, path_to_goal)


random.seed()   # To become true random, a different seed is used! (clock time)


def initial_project():
    history_list = []
    history_list_handicaps = []
    penalty = -1
    while True:

            c.send_request("command", "set_steps")

            n_fitness = 0
            s_fitness = 0
            e_fitness = 0
            o_fitness = 0
            try:
                posicao_atual = c.send_request("info", "position")

            except ValueError as excepcao_erro:
                print("Valor invalido ou nulo", excepcao_erro)
            cord_x = int(posicao_atual[1])
            cord_y = int(posicao_atual[4])
            history_list.append([cord_x, cord_y])
            penalty = penalty * 2
            history_list_handicaps.append(penalty)
            print("LISTA:", history_list)
            print("PENALTYS: ", history_list_handicaps)
            print([cord_x, cord_y])
    # ------------------------------------Make the agent look around the current position

            oeste = c.send_request("info", "west")

            norte = c.send_request("info", "north")

            este = c.send_request("info", "east")

            sul = c.send_request("info", "south")

    # ------------------------------------------------------------------------------------------------------------
            print("LISTA:", history_list)

            print("NORTE:", norte)
            print("OESTE:", oeste)
            print("SUL:", sul)
            print("ESTE:", este)
            print("posicao atual:", posicao_atual)
    # ---------------------------Secçao de codigo abaixo serve para o agente identificar o que viu e atribuir o fitness
            if norte == "['obstacle']":
                n_fitness = -9999999
                print("Obstacle found!")
            elif [cord_x, cord_y - 1] in history_list:

                n_fitness = history_list_handicaps[history_list.index([cord_x, cord_y - 1])]
                print("NORTH")
            elif norte == "['']":
                 n_fitness = -10
                 print("Empty position!")

            if este == "['obstacle']":
                e_fitness = -9999999
                print("Encontrei obstaculo")
            elif [cord_x + 1, cord_y] in history_list:
                e_fitness = history_list_handicaps[history_list.index([cord_x + 1, cord_y])]
                print("ja passei por aqui")
            elif este == "['']":
                e_fitness = -10
                print("Casa vazia")

            if sul == "['obstacle']":
                s_fitness = -9999999
                print("Encontrei obstaculo")
            elif [cord_x, cord_y + 1] in history_list:
                s_fitness = history_list_handicaps[history_list.index([cord_x, cord_y + 1])]
                print("ja passei por aqui")
            elif sul == "['']":
                s_fitness = -10
                print("Casa vazia")

            if oeste == "['obstacle']":
                o_fitness = -9999999
                print("Encontrei obstaculo")
            elif [cord_x - 1, cord_y] in history_list:
                o_fitness = history_list_handicaps[history_list.index([cord_x - 1, cord_y])]
                print("ja passei por aqui")
            elif oeste == "['']":
                o_fitness = -10
                print("Casa vazia")
    # ------------------------------------------------------------------------------------------------------------------

            print(".................................................................................................")
            print("n_fitness:", n_fitness)
            print("o_fitness:", o_fitness)
            print("s_fitness:", s_fitness)
            print("e_fitness:", e_fitness)
            print(".................................................................................................")

    # ----------------------Secçao de codigo abaixo serve pro cliente se movimentar tendo em conta os valores do fitness

            # -----Casos em qe existem 3 possiveis caminhos-----------------------

            if n_fitness > e_fitness and n_fitness == s_fitness and n_fitness == o_fitness:
                rand = random.randint(0, 2)

                if rand == 0:  # North
                    c.send_request("command", "north")
                elif rand == 1:  # South
                    c.send_request("command", "south")
                elif rand == 2:  # West
                    c.send_request("command", "west")
            elif n_fitness == e_fitness and n_fitness > s_fitness and n_fitness == o_fitness:
                rand = random.randint(0, 2)
                if rand == 0:  # North
                    c.send_request("command", "north")
                elif rand == 1:  # East
                    c.send_request("command", "east")
                elif rand == 2:  # West
                    c.send_request("command", "west")

            elif n_fitness == e_fitness and n_fitness == s_fitness and n_fitness > o_fitness:
                rand = random.randint(0, 2)

                if rand == 0:  # North
                    c.send_request("command", "north")
                elif rand == 1:  # South
                    c.send_request("command", "south")
                elif rand == 2:  # East
                    c.send_request("command", "east")

            elif s_fitness > n_fitness and s_fitness == e_fitness and s_fitness == o_fitness:
                rand = random.randint(0, 2)
                if rand == 0:  # South
                    c.send_request("command", "south")
                elif rand == 1:  # East
                    c.send_request("command", "east")
                elif rand == 2:  # West
                    c.send_request("command", "west")

            # -----Casos em qe existem 2 possiveis caminhos-----------------------

            elif n_fitness > e_fitness and n_fitness == s_fitness and n_fitness > o_fitness:
                rand = random.randint(0, 1)

                if rand == 0:  # Norte
                    c.send_request("command", "north")
                elif rand == 1:  # Sul
                    c.send_request("command", "south")

            elif n_fitness > e_fitness and n_fitness > s_fitness and n_fitness == o_fitness:
                rand = random.randint(0, 1)

                if rand == 0:  # Norte
                    c.send_request("command", "north")
                elif rand == 1:  # Oeste
                    c.send_request("command", "west")

            elif n_fitness == e_fitness and n_fitness > s_fitness and n_fitness > o_fitness:
                rand = random.randint(0, 1)

                if rand == 0:  # Norte
                    c.send_request("command", "north")
                elif rand == 1:  # Este
                    c.send_request("command", "east")

            elif s_fitness > e_fitness and s_fitness > n_fitness and s_fitness == o_fitness:
                rand = random.randint(0, 1)

                if rand == 0:  # Sul
                    c.send_request("command", "south")
                elif rand == 1:  # Oeste
                    c.send_request("command", "west")

            elif s_fitness == e_fitness and s_fitness > n_fitness and s_fitness > o_fitness:
                rand = random.randint(0, 1)

                if rand == 0:  # Sul
                    c.send_request("command", "south")
                elif rand == 1:  # Este
                    c.send_request("command", "east")

            elif o_fitness == e_fitness and o_fitness > n_fitness and o_fitness > s_fitness:
                rand = random.randint(0, 1)

                if rand == 0:  # Oeste
                    c.send_request("command", "west")
                elif rand == 1:  # Este
                    c.send_request("command", "east")

            # ------------casos em que somente existe 1 direcao certa---------
            elif n_fitness >= e_fitness and n_fitness >= s_fitness and n_fitness >= o_fitness:
                c.send_request("command", "north")
            elif e_fitness >= n_fitness and e_fitness >= s_fitness and e_fitness >= o_fitness:
                c.send_request("command", "east")
            elif s_fitness >= n_fitness and s_fitness >= e_fitness and s_fitness >= o_fitness:
                c.send_request("command", "south")
            elif o_fitness >= n_fitness and o_fitness >= e_fitness and o_fitness >= s_fitness:
                c.send_request("command", "west")

    # ------------------------------------------------------------------------------------------------------------------


def trepa_colinas():

        contador_tentativas = 0
        goal_raw = c.send_request("info", "goal")
        goal = [int(goal_raw[1]), int(goal_raw[4])]
        posicao_inicial_str = c.send_request("info", "position")
        posicao_inicial_int = [int(posicao_inicial_str[1]), int(posicao_inicial_str[4])]
        print("--------------")
        print(posicao_inicial_int)
        print(goal)
        print("--------------")

        while not(posicao_inicial_int[0] == goal[0] and posicao_inicial_int[1] == goal[1]):

            try:

                lista_de_possibilidades = [c.send_request("info", "north"),
                                           c.send_request("info", "south"),
                                           c.send_request("info", "west"),
                                           c.send_request("info", "east")]

                print(lista_de_possibilidades)
                if posicao_inicial_int[0] != goal[0]:
                    print("ENTROU X")
                    if posicao_inicial_int[0] > goal[0]:
                        if lista_de_possibilidades[3] == "['obstacle']":
                            print("obstaculo a frente")
                            posicao_inicial_int[0] -= 1
                        elif lista_de_possibilidades[3] == "['bomb']":
                            print("bomba a frente")
                        else:
                            c.send_request("command", "west")
                            posicao_inicial_int[0] -= 1

                    if posicao_inicial_int[0] < goal[0]:
                        if lista_de_possibilidades[2] == "['obstacle']":
                            print("obstaculo a frente")
                        elif lista_de_possibilidades[2] == "['bomb']":
                            print("bomba a frente")
                        else:
                            c.send_request("command", "east")
                            posicao_inicial_int[0] += 1
                if posicao_inicial_int[1] != goal[1]:
                    if posicao_inicial_int[1] > goal[1]:
                        if lista_de_possibilidades[0] == "['obstacle']":
                            print("obstaculo a frente")
                        elif lista_de_possibilidades[0] == "['bomb']":
                            print("bomba a frente")
                        else:
                            c.send_request("command", "north")
                            posicao_inicial_int[1] -= 1

                    if posicao_inicial_int[1] < goal[1]:
                        if lista_de_possibilidades[1] == "['obstacle']":
                            print("obstaculo a frente")
                            contador_tentativas += 1
                            if contador_tentativas > 3:
                                print("entrei")
                                rand = random.randint(0, 3)
                                if rand == 0:

                                    posicao_inicial_int[0] -= 1
                                    c.send_request("command", "west")
                                    posicao_atual_server = c.send_request("info", "position")
                                    print("Nao me consigo mover! Obstaculo?", "Posicao Cliente: ", posicao_inicial_int,
                                          "Posicao Servidor", posicao_atual_server)

                                    if not(posicao_atual_server[1] == str(posicao_inicial_int[0]) and
                                           posicao_atual_server[4] == str(posicao_inicial_int[1])):
                                        posicao_inicial_int[0] += 1

                                elif rand == 1:
                                    posicao_inicial_int[0] += 1
                                    c.send_request("command", "east")
                                    posicao_atual_server = c.send_request("info", "position")
                                    print("Nao me consigo mover! Obstaculo?", "Posicao Cliente: ", posicao_inicial_int,
                                          "Posicao Servidor", posicao_atual_server)
                                    if not (posicao_atual_server[1] == str(posicao_inicial_int[0]) and
                                            posicao_atual_server[4] == str(posicao_inicial_int[1])):

                                        posicao_inicial_int[0] -= 1
                                elif rand == 2:
                                        posicao_inicial_int[1] -= 1
                                        c.send_request("command", "north")
                                        posicao_atual_server = c.send_request("info", "position")
                                        print("Nao me consigo mover! Obstaculo?", "Posicao Cliente: ",
                                              posicao_inicial_int, "Posicao Servidor", posicao_atual_server)

                                        if not (posicao_atual_server[1] == str(posicao_inicial_int[0]) and
                                                posicao_atual_server[4] == str(posicao_inicial_int[1])):

                                            posicao_inicial_int[1] += 1
                                elif rand == 3:
                                        posicao_inicial_int[1] += 1
                                        c.send_request("command", "south")
                                        posicao_atual_server = c.send_request("info", "position")
                                        print("Nao me consigo mover! Obstaculo?", "Posicao Cliente: ",
                                              posicao_inicial_int, "Posicao Servidor", posicao_atual_server)

                                        if not (posicao_atual_server[1] == str(posicao_inicial_int[0]) and
                                                posicao_atual_server[4] == str(posicao_inicial_int[1])):

                                            posicao_inicial_int[1] -= 1

                                contador_tentativas = 0
                        elif lista_de_possibilidades[1] == "['bomb']":
                            print("bomba a frente")
                        else:
                            c.send_request("command", "south")
                            posicao_inicial_int[1] += 1

            except ConnectionError as excepcao_erro:
                print("Server ligado?", excepcao_erro)

        print("--------------")
        print(posicao_inicial_int)
        print(goal)
        print("--------------")

        messagebox.showinfo("Victory", "Goal Achieved")

        exit()


x = -1000
while x != 0:

    try:
        x = int(input("Digite: \n (1) - Teste Inicial \n (2) - Pesquisa em profundidade \n (3) - Trepa Colinas\n "
                      "Input: "))
        if x == 1:
            initial_project()
        elif x == 2:
            print("Work in Progress")
        elif x == 3:
            trepa_colinas()
        else:
            print("Valor inexitente ou errado!")
    except ValueError as excepcao_erro:
        print("Valor inexitente ou errado!", excepcao_erro)


'''
x = 0
while x <40:
    c.execute("command", "east")
    x = x + 1
'''

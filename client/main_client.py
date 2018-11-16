import client
import ast
import random
from tkinter import messagebox
c = client.Client('127.0.0.1', 50000)
res = c.connect()
random.seed()   # To become true random, a different seed is used! (clock time)
def projeto_inicial():
    lista_history = []
    lista_history_penaltys = []
    penalty = -1

    if res != -1:
        while True:

            c.execute("command", "set_steps")

            sul = ""
            oeste = ""
            norte = ""
            este = ""

            n_fitness = 0
            s_fitness = 0
            e_fitness = 0
            o_fitness = 0
            try:
                posicao_atual = c.execute("info", "position")

            except ValueError as excepcao_erro:
                print("Valor invalido ou nulo", excepcao_erro)
            cord_x = int(posicao_atual[1])
            cord_y = int(posicao_atual[4])
            lista_history.append([cord_x, cord_y])
            penalty = penalty * 2
            lista_history_penaltys.append(penalty)
            print("LISTA:", lista_history)
            print("PENALTYS: ", lista_history_penaltys)
            print([cord_x, cord_y])
    #------------------------------------Secção de codigo abaixo serve para o agente ver ao seu redor

            oeste = c.execute("info", "west")

            norte = c.execute("info", "north")

            este = c.execute("info", "east")

            sul = c.execute("info", "south")

    #------------------------------------------------------------------------------------------------------------
            print("LISTA:", lista_history)

            print("NORTE:", norte)
            print("OESTE:", oeste)
            print("SUL:", sul)
            print("ESTE:", este)
            print("posicao atual:", posicao_atual)
    #---------------------------Secçao de codigo abaixo serve para o agente identificar o que viu e atribuir o fitness--------------------------------
            if norte == "['obstacle']":
                n_fitness = -9999999
                print("Encontrei obstaculo")
            elif [cord_x, cord_y - 1] in lista_history:

                n_fitness = lista_history_penaltys[lista_history.index([cord_x, cord_y - 1])]
                print("NORTEEEEEEEEEEEEEEEEEEEEEEEEEEE")
            elif norte == "['']":
                 n_fitness = -10
                 print("Casa vazia")

            if este == "['obstacle']":
                e_fitness = -9999999
                print("Encontrei obstaculo")
            elif [cord_x + 1, cord_y] in lista_history:
                e_fitness = lista_history_penaltys[lista_history.index([cord_x +1, cord_y])]
                print("ja passei por aqui")
            elif este == "['']":
                e_fitness = -10
                print("Casa vazia")

            if sul == "['obstacle']":
                s_fitness = -9999999
                print("Encontrei obstaculo")
            elif [cord_x, cord_y + 1] in lista_history:
                s_fitness = lista_history_penaltys[lista_history.index([cord_x, cord_y +1])]
                print("ja passei por aqui")
            elif sul == "['']":
                s_fitness = -10
                print("Casa vazia")

            if oeste == "['obstacle']":
                o_fitness = -9999999
                print("Encontrei obstaculo")
            elif [cord_x - 1, cord_y] in lista_history:
                o_fitness = lista_history_penaltys[lista_history.index([cord_x - 1, cord_y])]
                print("ja passei por aqui")
            elif oeste == "['']":
                o_fitness = -10
                print("Casa vazia")
    #----------------------------------------------------------------------------------------------------------------------


            print(".......................................................................................................")
            print("n_fitness:", n_fitness)
            print("o_fitness:", o_fitness)
            print("s_fitness:", s_fitness)
            print("e_fitness:", e_fitness)
            print(".......................................................................................................")

    #-------------------------------Secçao de codigo abaixo serve pro cliente se movimentar tendo em conta os valores do fitness---

            #-----Casos em qe existem 3 possiveis caminhos-----------------------

            if n_fitness > e_fitness and n_fitness == s_fitness and n_fitness == o_fitness:
                rand = random.randint(0,2)

                if rand == 0: #Norte
                    c.execute("command", "north")
                elif rand == 1:#Sul
                    c.execute("command", "south")
                elif rand ==  2:#Oeste
                    c.execute("command", "west")
            elif n_fitness == e_fitness and n_fitness > s_fitness and n_fitness == o_fitness:
                rand = random.randint(0,2)
                if rand == 0:  # Norte
                    c.execute("command", "north")
                elif rand == 1:  # Este
                    c.execute("command", "east")
                elif rand == 2:  # Oeste
                    c.execute("command", "west")

            elif n_fitness == e_fitness and n_fitness == s_fitness and n_fitness > o_fitness:
                rand = random.randint(0,2)

                if rand == 0:  # Norte
                    c.execute("command", "north")
                elif rand == 1:  # SUL
                    c.execute("command", "south")
                elif rand == 2:  # Este
                    c.execute("command", "east")


            elif s_fitness > n_fitness and s_fitness == e_fitness and s_fitness == o_fitness:
                rand = random.randint(0,2)
                if rand == 0:  # Sul
                    c.execute("command", "south")
                elif rand == 1:  # Este
                    c.execute("command", "east")
                elif rand == 2:  # Oeste
                    c.execute("command", "west")


            # -----Casos em qe existem 2 possiveis caminhos-----------------------


            elif n_fitness > e_fitness and n_fitness == s_fitness and n_fitness > o_fitness:
                rand = random.randint(0, 1)

                if rand == 0:  # Norte
                    c.execute("command", "north")
                elif rand == 1:  # Sul
                    c.execute("command", "south")

            elif n_fitness > e_fitness and n_fitness > s_fitness and n_fitness == o_fitness:
                rand = random.randint(0, 1)

                if rand == 0:  # Norte
                    c.execute("command", "north")
                elif rand == 1:  # Oeste
                    c.execute("command", "west")

            elif n_fitness == e_fitness and n_fitness > s_fitness and n_fitness > o_fitness:
                rand = random.randint(0, 1)

                if rand == 0:  # Norte
                    c.execute("command", "north")
                elif rand == 1:  # Este
                    c.execute("command", "east")

            elif s_fitness > e_fitness and s_fitness > n_fitness and s_fitness == o_fitness:
                rand = random.randint(0, 1)

                if rand == 0:  # Sul
                    c.execute("command", "south")
                elif rand == 1:  # Oeste
                    c.execute("command", "west")

            elif s_fitness == e_fitness and s_fitness > n_fitness and s_fitness > o_fitness:
                rand = random.randint(0, 1)

                if rand == 0:  # Sul
                    c.execute("command", "south")
                elif rand == 1:  # Este
                    c.execute("command", "east")

            elif o_fitness == e_fitness and o_fitness > n_fitness and o_fitness > s_fitness:
                rand = random.randint(0, 1)

                if rand == 0:  # Oeste
                    c.execute("command", "west")
                elif rand == 1:  # Este
                    c.execute("command", "east")


            #------------casos em que somente existe 1 direcao certa---------
            elif n_fitness >= e_fitness and n_fitness >= s_fitness and n_fitness >= o_fitness:
                c.execute("command", "north")
            elif e_fitness >= n_fitness and e_fitness >= s_fitness and e_fitness >= o_fitness:
                c.execute("command", "east")
            elif s_fitness >= n_fitness and s_fitness >= e_fitness and s_fitness >= o_fitness:
                c.execute("command", "south")
            elif o_fitness >= n_fitness and o_fitness >= e_fitness and o_fitness >= s_fitness:
                c.execute("command", "west")

    #----------------------------------------------------------------------------------------------------------------------------


def trepa_colinas():

        contador_tentativas = 0
        x = c.execute("info", "goal")
        goal = [int(x[1]), int(x[4])]
        posicao_inicial_str = c.execute("info", "position")
        posicao_inicial_int = [int(posicao_inicial_str[1]), int(posicao_inicial_str[4])]
        print("--------------")
        print(posicao_inicial_int)
        print(goal)
        print("--------------")

        while not(posicao_inicial_int[0] == goal[0] and posicao_inicial_int[1] == goal[1]):

            try:

                lista_de_possibilidades =[c.execute("info", "north"),
                                        c.execute("info", "south"),
                                        c.execute("info", "west"),
                                        c.execute("info", "east")]

                print(lista_de_possibilidades)
                aleatorio = random.randint(0,1)
                if aleatorio == 0:
                    if posicao_inicial_int[0] != goal[0]:
                        print("ENTROU X")
                        if posicao_inicial_int[0] > goal[0]:
                            if lista_de_possibilidades[3] == ("['obstacle']"):
                                print("obstaculo a frente")
                                contador_tentativas += 1
                                if contador_tentativas > 3:
                                    print("entrei")
                                    rand = random.randint(0, 2)
                                    if rand == 0:
                                        if lista_de_possibilidades[3] != ("['obstacle']"):
                                            posicao_inicial_int[0] += 1
                                            c.execute("command", "east")

                                    elif rand == 1:
                                        if lista_de_possibilidades[0] != ("['obstacle']"):
                                            posicao_inicial_int[1] -= 1
                                            c.execute("command", "north")

                                    elif rand == 2:
                                        if lista_de_possibilidades[1] != ("['obstacle']"):
                                            posicao_inicial_int[1] += 1
                                            c.execute("command", "south")


                                    contador_tentativas = 0
                                posicao_inicial_int[0] -= 1
                            elif lista_de_possibilidades[3] == ("['bomb']"):
                                print("bomba a frente")
                            else:
                                c.execute("command", "west")
                                posicao_inicial_int[0] -= 1


                        if posicao_inicial_int[0] < goal[0]:
                            if lista_de_possibilidades[2] == ("['obstacle']"):
                                print("obstaculo a frente")
                                contador_tentativas += 1
                                if contador_tentativas > 3:
                                    print("entrei")
                                    rand = random.randint(0, 2)
                                    if rand == 0:
                                        if lista_de_possibilidades[2] != ("['obstacle']"):
                                            posicao_inicial_int[0] -= 1
                                            c.execute("command", "west")

                                    elif rand == 1:
                                        if lista_de_possibilidades[0] != ("['obstacle']"):
                                            posicao_inicial_int[1] -= 1
                                            c.execute("command", "north")

                                    elif rand == 2:
                                        if lista_de_possibilidades[1] != ("['obstacle']"):
                                            posicao_inicial_int[1] += 1
                                            c.execute("command", "south")


                                    contador_tentativas = 0
                            elif lista_de_possibilidades[2] == ("['bomb']"):
                                print("bomba a frente")
                            else:
                                c.execute("command", "east")
                                posicao_inicial_int[0] += 1
                elif aleatorio == 1:
                    if posicao_inicial_int[1] != goal[1]:
                        if posicao_inicial_int[1] > goal[1]:
                            if lista_de_possibilidades[0] == ("['obstacle']"):
                                print("obstaculo a frente")
                                contador_tentativas += 1
                                if contador_tentativas > 3:
                                    print("entrei")
                                    rand = random.randint(0, 2)
                                    if rand == 0:
                                        if lista_de_possibilidades[2] != ("['obstacle']"):
                                            posicao_inicial_int[0] -= 1
                                            c.execute("command", "west")

                                    elif rand == 1:
                                        if lista_de_possibilidades[3] != ("['obstacle']"):
                                            posicao_inicial_int[0] += 1
                                            c.execute("command", "east")


                                    elif rand == 2:
                                        if lista_de_possibilidades[1] != ("['obstacle']"):
                                            posicao_inicial_int[1] += 1
                                            c.execute("command", "south")


                                    contador_tentativas = 0
                            elif lista_de_possibilidades[0] == ("['bomb']"):
                                print("bomba a frente")
                            else:
                                c.execute("command", "north")
                                posicao_inicial_int[1] -= 1

                        if posicao_inicial_int[1] < goal[1]:
                            if lista_de_possibilidades[1] == ("['obstacle']"):
                                print("obstaculo a frente")
                                contador_tentativas += 1
                                if contador_tentativas > 3:
                                    print("entrei")
                                    rand = random.randint(0,2)
                                    if rand == 0:
                                        if lista_de_possibilidades[2] != ("['obstacle']"):
                                            posicao_inicial_int[0] -= 1
                                            c.execute("command", "west")


                                    elif rand == 1:
                                        if lista_de_possibilidades[3] != ("['obstacle']"):
                                            posicao_inicial_int[0] += 1
                                            c.execute("command", "east")



                                    elif rand == 2:
                                        if lista_de_possibilidades[0] != ("['obstacle']"):
                                            posicao_inicial_int[1] -= 1
                                            c.execute("command", "north")



                                    contador_tentativas = 0
                            elif lista_de_possibilidades[1] == ("['bomb']"):
                                print("bomba a frente")
                            else:
                                c.execute("command", "south")
                                posicao_inicial_int[1] += 1
                            print("POSICAO: ", posicao_inicial_int)
                print("--------------")
                print(posicao_inicial_int)
                print(goal)
                print("--------------")





            except ConnectionError as excepcao_erro:
                print("Server ligado?",excepcao_erro)


        messagebox.showinfo("Vitoria", "Goal Archieved")

        exit()




x = -1000
while x != 0:

    try:
        x = int(input("Digite: \n (1) - Teste Inicial \n (2) - Pesquisa em profundidade \n (3) - Trepa Colinas"))
        if x == 1:
            projeto_inicial()
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
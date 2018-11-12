import client
import ast
import random

c = client.Client('127.0.0.1', 50000)
res = c.connect()
random.seed()   # To become ltrue random, a different seed is used! (clock time)

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
        direc = " "
        x = 1

        while x < 5:  #Scan da area
              direc = c.execute("info", "direction")

              if direc == "west":
                  oeste = c.execute("info", "view")
              elif direc == "north":
                  norte = c.execute("info", "view")
              elif direc == "east":
                  este = c.execute("info", "view")
              elif direc == "south":
                  sul = c.execute("info", "view")

              c.execute("command", "right")

              x = x + 1
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







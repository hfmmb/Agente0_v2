import client
import ast
import random

c = client.Client('127.0.0.1', 50000)
res = c.connect()
random.seed()   # To become ltrue random, a different seed is used! (clock time)

lista_history = []

if res != -1:
    while True:

        c.execute("command", "set_steps")
        x = 1
        sul = ""
        oeste = ""
        norte = ""
        este = ""

        n_fitness = 0
        s_fitness = 0
        e_fitness = 0
        o_fitness = 0
        posicao_atual = c.execute("info", "position")

        cord_x = int(posicao_atual[1])
        cord_y = int(posicao_atual[4])
        lista_history.append([cord_x, cord_y])
        print("LISTA:", lista_history)
        print([cord_x, cord_y])



        while x < 4:  #Scan da area
              c.execute("command", "right")

              if x == 4:
                  este = c.execute("info", "view")
              elif x == 3:
                  norte = c.execute("info", "view")
              elif x == 2:
                  oeste = c.execute("info", "view")
              elif x == 1:
                  sul = c.execute("info", "view")

              x = x + 1
        print("LISTA:", lista_history)

        print("NORTE:", norte)
        print("OESTE:", oeste)
        print("SUL:", sul)
        print("ESTE:", este)
        print("posicao atual:", posicao_atual)

        if norte == "['obstacle']":
            n_fitness = -9999999
            print("Encontrei obstaculo")
        elif [cord_x, cord_y - 1] in lista_history:
            n_fitness = -20
            print("ja passei por aqui")
        elif norte == "['']":
             n_fitness = -10
             print("Casa vazia")

        if este == "['obstacle']":
            e_fitness = -9999999
            print("Encontrei obstaculo")
        elif [cord_x + 1, cord_y] in lista_history:
            e_fitness = -20
            print("ja passei por aqui")
        elif este == "['']":
            e_fitness = -10
            print("Casa vazia")

        if sul == "['obstacle']":
            s_fitness = -9999999
            print("Encontrei obstaculo")
        elif [cord_x, cord_y + 1] in lista_history:
            s_fitness = -20
            print("ja passei por aqui")
        elif sul == "['']":
            s_fitness = -10
            print("Casa vazia")

        if oeste == "['obstacle']":
            o_fitness = -9999999
            print("Encontrei obstaculo")
        elif [cord_x - 1, cord_y] in lista_history:
            o_fitness = -20
            print("ja passei por aqui")
        elif oeste == "['']":
            o_fitness = -10
            print("Casa vazia")


        print(".......................................................................................................")
        print("n_fitness:", n_fitness)
        print("o_fitness:", o_fitness)
        print("s_fitness:", s_fitness)
        print("e_fitness:", e_fitness)
        print(".......................................................................................................")
        if n_fitness >= e_fitness and n_fitness >= s_fitness and n_fitness >= o_fitness:
            c.execute("command", "north")
        elif e_fitness >= n_fitness and e_fitness >= s_fitness and e_fitness >= o_fitness:
            c.execute("command", "east")
        elif s_fitness >= n_fitness and s_fitness >= e_fitness and s_fitness >= o_fitness:
            c.execute("command", "south")
        elif o_fitness >= n_fitness and o_fitness >= e_fitness and o_fitness >= s_fitness:
            c.execute("command", "west")







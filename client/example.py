import client
import ast
import random

c = client.Client('127.0.0.1', 50000)
res = c.connect()
random.seed()   # To become true random, a different seed is used! (clock time)

lista_history = []

if res != -1:
    while True:
        lista_history.append(c.execute("info", "position"))
        c.execute("command", "set_steps")
        c.execute("command",   "east")
        x = 0
        c.execute("info", "map")
        while x < 4:
          c.execute("command", "right")
          c.execute("info", "view")
          x = x + 1
        print("LISTA:", lista_history)

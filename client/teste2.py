import client
import ast
import random
from tkinter import messagebox
c = client.Client('127.0.0.1', 50000)
res = c.connect()
random.seed()   # To become true random, a different seed is used! (clock time)

x = 0
while x < 40:
    print("quase")
    c.execute("command", "south")
    print("after")
    x = x + 1
print("finito")
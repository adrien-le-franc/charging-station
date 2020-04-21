import numpy as np
import os
from numpy.random import randint
from player import Player

Player = Player()

for t in range(48):
    Player.observe(t,{"departures" : [15,15,15,15],"arrivals": [35,35,35,35]},{"internal":0,"external_sale":0,"external_purchase":0},0)
    load = Player.compute_load(t)
    Player.penalty(t)
    print (load)
print(Player.bill)
print(Player.battery_stock)

print("tests passed !")

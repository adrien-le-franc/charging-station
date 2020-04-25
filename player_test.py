import numpy as np
import os
from numpy.random import randint
from player import Player

Player = Player()

for t in range(48):
    if t==12:
        Player.observe(t,{"departures" : [1,1,1,1],"arrivals": [0,0,0,0]},{"internal":0,"external_sale":0,"external_purchase":0},0)
    elif t==36:
        Player.observe(t,{"departures" : [0,0,0,0],"arrivals": [1,1,1,1]},{"internal":0,"external_sale":0,"external_purchase":0},0)
    else:
        Player.observe(t,{"departures" : [0,0,0,0],"arrivals": [0,0,0,0]},{"internal":0,"external_sale":0,"external_purchase":0},0)
    load = Player.compute_load(t,0)
    Player.penalty(t)
    print(load)

print(Player.depart)
print(Player.arrival)
print("load",Player.load_battery_periode)
print(Player.bill)
print(Player.battery_stock)
print(Player.depart)


print("tests passed !")

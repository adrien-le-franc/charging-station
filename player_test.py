import numpy as np
import os
from numpy.random import randint
from player import Player

Player = Player()

for t in range(48):
    load = Player.compute_load(t,{"departures" : [1,1,1,1],"arrivals": [0,0,0,0]})
    if t==12:
        load = Player.compute_load(t,{"departures" : [1,1,1,1],"arrivals": [0,0,0,0]})
    elif t==36:
        load = Player.compute_load(t,{"departures" : [0,0,0,0],"arrivals": [1,1,1,1]})
    else:
        load = Player.compute_load(t,{"departures" : [0,0,0,0],"arrivals": [0,0,0,0]})

    Player.penalty(t)
    print(load)

print(Player.depart)
print(Player.arrival)
print("load",Player.load_battery_periode)
print(Player.bill)
print(Player.battery_stock)
print(Player.depart)

new_bat = np.concatenate((Player.battery_stock["slow"],Player.battery_stock["fast"]),axis=1)
new_bat = np.transpose(new_bat)
print(new_bat)


print("tests passed !")

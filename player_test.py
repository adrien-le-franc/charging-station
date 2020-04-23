import numpy as np
import os
from numpy.random import randint
from player import Player

Player = Player()

for t in range(48):

    Player.observe(t,{"departures" : [0,0,0,0],"arrivals": [0,0,0,0]},{"internal":0,"external_sale":0,"external_purchase":0},0)
    load = Player.compute_load(t,0)
    Player.nb_cars(0)
    Player.penalty(t)
    print ("load",load)
    print ("p_station",Player.p_station)
print("load",Player.load_battery_periode)
print(Player.bill)
print(Player.battery_stock)
print(Player.depart)


print("tests passed !")

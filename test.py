import numpy as np
import os
from numpy.random import randint
from player import Player

player = Player()

for t in range(48):
    load = player.compute_load(t,{"departures" : [1,1,1,1],"arrivals": [0,0,0,0]})
    if t==12:
        load = player.compute_load(t,{"departures" : [1,1,1,1],"arrivals": [0,0,0,0]})
    elif t==36:
        load = player.compute_load(t,{"departures" : [0,0,0,0],"arrivals": [1,1,1,1]})
    else:
        load = player.compute_load(t,{"departures" : [0,0,0,0],"arrivals": [0,0,0,0]})

    soc = player.battery_stock
    assert soc['slow'][t][0] >= 0
    assert soc['slow'][t][0] <= 40
    assert soc['slow'][t][1] >= 0
    assert soc['slow'][t][1] <= 40
    assert soc['fast'][t][0] >= 0
    assert soc['fast'][t][0] <= 40
    assert soc['fast'][t][1] >= 0
    assert soc['fast'][t][1] <= 40
    player.penalty(t)

print("tests passed !")

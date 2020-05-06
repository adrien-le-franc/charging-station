import numpy as np
import os
from numpy.random import randint
from player import Player

player = Player()

for t in range(48):

    if t==12:
        data = {"departures" : [1,1,1,1],"arrivals": [0,0,0,0]}
    elif t==36:
        data = {"departures" : [0,0,0,0],"arrivals": [1,1,1,1]}
    else:
        data = {"departures" : [0,0,0,0],"arrivals": [0,0,0,0]}

    player.compute_load(t, data)
    prices = {"purchase" : 0.06,"sale" : 0.03}
    imbalance = {"purchase_cover":0.02, "sale_cover": 0.02}
    player.observe(t, data, prices, imbalance)

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

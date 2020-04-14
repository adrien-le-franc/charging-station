import numpy as np
import os
from numpy.random import randint
from charging_station import ChargingStation

charging_station = ChargingStation()

for t in range(48):
    load = charging_station.compute_load(t)
    charging_station.observe(t,0,0)
    charging_station.penality(t)
    print (load)
print(charging_station.battery_stock)

print("tests passed !")

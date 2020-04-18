import numpy as np
import os
from numpy.random import randint
from charging_station import ChargingStation

charging_station = ChargingStation()

for t in range(48):
    charging_station.observe(t,{"departures" : [15,15,15,15],"arrivals": [35,35,35,35]},{"internal":0,"external_sale":0,"external_purchase":0},0)
    load = charging_station.compute_load(t)
    charging_station.penalty(t)
    print (load)
print(charging_station.bill)
print(charging_station.battery_stock)

print("tests passed !")

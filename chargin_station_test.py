import numpy as np
import os
from numpy.random import randint
from charging_station import ChargingStation


CS = ChargingStation()
t = 0
load_battery = {"fast" : np.zeros((48,2)),"slow" : np.zeros((48,2))}
load_battery = CS.update_batterie_stock(t,load_battery)
print(load_battery)


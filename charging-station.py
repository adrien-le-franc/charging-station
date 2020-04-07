import numpy as np
import os
from numpy.random import randint


## Charging Station

class ChargingStation:

    def __init__(self):
        self.dt = 0.5
        self.efficiency = 0.95
        self.scenario = {}
        self.bill = np.zeros(48) # Where 5e penalities will be stocked
        self.load = np.zeros(48) # List l4
        self.load_batterie = {"fast" : np.zeros((48,2)),"slow" : np.zeros((48,2))} # How the player wants to charge/discharge the veicules
        self.battery_stock = {"slow" : np.zeros((49,2)), "fast" : np.zeros((49,2))} # State of the batteries
        self.nb_fast = 2 # Number of Stations Fasts and Lows used
        self.nb_slow = 2
        self.pmax_fast = 22
        self.pmax_slow = 3
        self.cmax = 40*4 ## Maximal capacity of the CS when the 4 slots are used

    # Version naive : on suppose que toutes les voitures sont là 24/24 juste pour voir l'update de leur batteries
    # Donc deux voitures sur le fast et deux sur le slow et comme les voitures ne partent pas on oublie la pénalité de 5e si elle ne sont pas chargées suffisemment
    # Pas de V2G également

    def update_batterie_stock(self,time,load_battery):

        nb = {"slow" : self.nb_slow, "fast" : self.nb_fast}
        p_max = {"slow" : 3, "fast" : 22}
        c_max = {"slow" : 40, "fast" : 40}


        for speed in ["slow","fast"] :
            for i in range(2):
                if abs(load_battery[speed][time][i]) >= p_max[speed]:
                    load_battery[speed][time][i] = p_max[speed]*np.sign(load_battery[speed][time][i])
            # si on veut charger plus de power que possible on cap à pmax
            new_stock = { "slow" : [0,0], "fast" : [0,0] }

            new_stock["slow"][0] = self.battery_stock["slow"][time][0] + (self.efficiency*max(0,load_battery["slow"][time][0])+min(0,load_battery["slow"][time][0])/self.efficiency)*self.dt
            new_stock["slow"][1] = self.battery_stock["slow"][time][1] + (self.efficiency*max(0,load_battery["slow"][time][1])+min(0,load_battery["slow"][time][1])/self.efficiency)*self.dt
            # We update the new stock of each batteries "slow"

            new_stock["fast"][0]=self.battery_stock["fast"][time][0] + (self.efficiency*max(0,load_battery["fast"][time][0])+min(0,load_battery["fast"][time][0])/self.efficiency)*self.dt
            new_stock["fast"][1]=self.battery_stock["fast"][time][1] + (self.efficiency*max(0,load_battery["fast"][time][1])+min(0,load_battery["fast"][time][1])/self.efficiency)*self.dt
            # We update the new stock of each batteries "fast"


        for speed in ["slow","fast"] :
            for i in range(2):
                if new_stock[speed][i] < 0:
                    load_battery[speed][time][i] = -(self.battery_stock[speed][time][i])/(self.efficiency*self.dt)
                    new_stock[speed][i] = 0
            # We can't discharge the batterie under 0

                elif new_stock[speed][i] > c_max[speed]:
                    load_battery[speed][time][i] = (c_max[speed] - self.battery_stock[speed][time][i] ) / (self.efficiency*self.dt)
                    new_stock[speed][i] = c_max[speed]
            # We can't charge the batteries over their maximum capacities

        for speed in ["slow","fast"] :
            for i in range(2):
                if abs(load_battery[speed][time][i]) >= p_max[speed] :
                    load_battery[speed][time][i] = p_max[speed]*np.sign(load_battery[speed][time][i])

        for speed in ["slow","fast"] :
            for i in range(2):
                self.battery_stock[speed][time+1][i]=new_stock[speed][i]
            # Update of batteries stocks

        return load_battery # We return load_battery clear of the player's potential mistakes



    def compute_load(self,time):

        load_battery = self.load_battery(time)
        load = self.update_batterie_stock(time, load_battery)
        for i in range(2):
            self.load[time] += load["slow"][i] + load["fast"][i]

##

CS = ChargingStation()
t = 0
load_battery = {"fast" : np.zeros((48,2)),"slow" : np.zeros((48,2))}
load_battery = CS.update_batterie_stock(t,load_battery)
print(load_battery)

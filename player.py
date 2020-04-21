import numpy as np
import os
from numpy.random import randint


## Charging Station

class Player:

    def __init__(self):
        self.dt = 0.5
        self.nb_t = int(24/self.dt)
        self.prices = {"internal" : [],"external_purchase" : [],"external_sale" : []}
        self.efficiency = 0.95
        self.bill = np.zeros(self.nb_t) # Where 5e penalities will be stocked
        self.load = np.zeros(self.nb_t) # List l4
        self.load_battery_periode = {"fast" : np.zeros((self.nb_t,2)),"slow" : np.zeros((self.nb_t,2))} # How the player wants to charge/discharge the veicules
        self.battery_stock = {"slow" : np.zeros((self.nb_t+1,2)), "fast" : np.zeros((self.nb_t+1,2))} # State of the batteries
        self.nb_fast_max = 2 # Number of Stations Fasts and Lows max
        self.nb_slow_max = 2
        self.nb_slow = 2 # Number of Stations Fast and Slow currently used
        self.nb_fast = 2
        self.pmax_fast = 22
        self.pmax_slow = 3
        self.cmax = 40*4 # Maximal capacity of the CS when the 4 slots are used
        self.depart = {"slow" : np.zeros(2), "fast" : np.zeros(2)} # Time of departure of every cars
        self.arrival = {"slow" : np.zeros(2), "fast" : np.zeros(2)} # Time of arrival of every cars
        self.here = {"slow" : np.ones(2), "fast" : np.ones(2)}
        self.imbalance=[]
        self.pmax_station = 22*2+3*2

    def update_battery_stock(self,time,load_battery):
        self.nb_cars(time) # We check what cars is here
        p_max = {"slow" : [3*self.here["slow"][0],3*self.here["slow"][1]], "fast" : [22*self.here["fast"][0],22*self.here["fast"][1]]}
        c_max = {"slow" : [40*self.here["slow"][0],40*self.here["slow"][1]], "fast" : [40*self.here["fast"][0],40*self.here["fast"][1]]}
        # p_max and c_max depend on whether the car is here or not.
        self.pmax_station=self.pmax_fast*self.nb_fast + self.pmax_slow*self.nb_slow
        for speed in ["slow","fast"] :
            for i in range(2):
                if abs(load_battery[speed][i]) >= p_max[speed][i]:
                    load_battery[speed][i] = p_max[speed][i]*np.sign(load_battery[speed][i])
            # Can't put more power than p_max
            new_stock = { "slow" : [0,0], "fast" : [0,0] }

            new_stock["slow"][0] = self.battery_stock["slow"][time][0] + (self.efficiency*max(0,load_battery["slow"][0])+min(0,load_battery["slow"][0])/self.efficiency)*self.dt
            new_stock["slow"][1] = self.battery_stock["slow"][time][1] + (self.efficiency*max(0,load_battery["slow"][1])+min(0,load_battery["slow"][1])/self.efficiency)*self.dt
            # We update the new stock of each batteries "slow"

            new_stock["fast"][0]=self.battery_stock["fast"][time][0] + (self.efficiency*max(0,load_battery["fast"][0])+min(0,load_battery["fast"][0])/self.efficiency)*self.dt
            new_stock["fast"][1]=self.battery_stock["fast"][time][1] + (self.efficiency*max(0,load_battery["fast"][1])+min(0,load_battery["fast"][1])/self.efficiency)*self.dt
            # We update the new stock of each batteries "fast"


        for speed in ["slow","fast"] :
            for i in range(2):
                if new_stock[speed][i] < 0:
                    load_battery[speed][i] = -(self.battery_stock[speed][time][i])/(self.efficiency*self.dt)
                    new_stock[speed][i] = 0
            # We can't discharge the batterie under 0

                elif new_stock[speed][i] > c_max[speed][i]:
                    load_battery[speed][i] = (c_max[speed][i] - self.battery_stock[speed][time][i] ) / (self.efficiency*self.dt)
                    new_stock[speed][i] = c_max[speed][i]
            # We can't charge the batteries over their maximum capacities

        for speed in ["slow","fast"] :
            for i in range(2):
                if abs(load_battery[speed][i]) >= p_max[speed][i]:
                    load_battery[speed][i] = p_max[speed][i]*np.sign(load_battery[speed][i])
            # Can't put more power than p_max

        for speed in ["slow","fast"] :
            for i in range(2):
                self.battery_stock[speed][time+1][i]=new_stock[speed][i]
            # Update of batteries stocks
                if time == self.arrival[speed][i]-1:
                    self.battery_stock[speed][time+1][i] = self.battery_stock[speed][int(self.depart[speed][i])][i]-4
                    # When the cars comes back it has lost 4 kWh in the battery
                self.load_battery_periode[speed][time][i] = load_battery[speed][i]

        return load_battery # We return load_battery clear of the player's potential mistakes




    def nb_cars(self,time):
        s = 0
        for i in range(self.nb_slow_max):
            if (self.depart["slow"][i]<time) and (self.arrival["slow"][i]>time):
                self.here["slow"][i]=0
            else:
                self.here["slow"][i]=1
                s+=1
        f = 0
        for j in range(self.nb_fast_max):
            if (self.depart["fast"][j]<time) and (self.arrival["fast"][j]>time):
                self.here["fast"][j]=0
            else:
                self.here["fast"][j]=1
                f+=1
        self.nb_slow = s
        self.nb_fast = f
        # Acctualise how many cars and which are at the station at t = time.


    def penalty(self,time):
        for speed in ["slow","fast"] :
            for i in range(2):
                if time == self.depart[speed][i] and self.battery_stock[speed][time][i]/40 < 25:
                    self.bill[time]+=5
        # If at the departure time of the veicule its battery isn't charged at least at 25% then you pay a 5e fine


    def take_decision(self, time):
        load_battery = {"fast" : 5*np.ones(2),"slow" : 5*np.ones(2)}
        # TO BE COMPLETED
        # Have to return load_battery to put in update_batterie_stock to get the load.
        # load_battery must be in the following format : {"fast" : [load_car_fast_1,load_car_fast_2],"slow" : [load_car_slow_1,load_car_slow_2]}
        return load_battery


    def observe(self, time, data, price, imbalance):

        self.depart["slow"][0]=data["departures"][0]
        self.depart["slow"][1]=data["departures"][1]
        self.depart["fast"][0]=data["departures"][2]
        self.depart["fast"][1]=data["departures"][3]

        self.arrival["slow"][0]=data["arrivals"][0]
        self.arrival["slow"][1]=data["arrivals"][1]
        self.arrival["fast"][0]=data["arrivals"][2]
        self.arrival["fast"][1]=data["arrivals"][3]

        if time>0:
            self.prices["internal"].append(price["internal"])
            self.prices["external_sale"].append(price["external_sale"])
            self.prices["external_purchase"].append(price["external_purchase"])

            self.imbalance.append(imbalance)


    def reset(self):
        self.bill = np.zeros(self.nb_t)
        self.load = np.zeros(self.nb_t)
        self.load_battery_periode = {"fast" : np.zeros((self.nb_t,2)),"slow" : np.zeros((self.nb_t,2))}
        self.battery_stock = {"slow" : np.zeros((self.nb_t+1,2)), "fast" : np.zeros((self.nb_t+1,2))}
        self.nb_slow = 2
        self.nb_fast = 2
        self.here = {"slow" : np.ones(2), "fast" : np.ones(2)}
        self.depart = {"slow" : np.zeros(2), "fast" : np.zeros(2)}
        self.arrival = {"slow" : np.zeros(2), "fast" : np.zeros(2)}
        self.prices = {"internal" : [],"external_purchase" : [],"external_sale" : []}
        self.imbalance=[]

    def compute_load(self,time):
        load_battery = self.take_decision(time) # How you charge or discharge is the players choice
        load = self.update_battery_stock(time, load_battery)
        for i in range(2):
            self.load[time] += load["slow"][i] + load["fast"][i]
        self.penalty(time)
        return self.load[time]

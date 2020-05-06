import numpy as np
import os
from numpy.random import randint


## Charging Station

class Player:

    def __init__(self):
        self.dt = 0.5
        self.horizon = int(24/self.dt)
        self.prices = {"purchase" : [],"sale" : []}
        self.efficiency = 0.95
        self.bill = np.zeros(self.horizon) # Where 5e penalities will be stocked
        self.load = np.zeros(self.horizon) # List l4
        self.load_battery_periode = {"fast" : np.zeros((self.horizon,2)),"slow" : np.zeros((self.horizon,2))} # How the player wants to charge/discharge the veicules
        self.battery_stock = {"slow" : np.zeros((self.horizon+1,2)), "fast" : np.zeros((self.horizon+1,2))} # State of the batteries
        self.nb_fast_max = 2 # Number of Stations Fasts and Lows max
        self.nb_slow_max = 2
        self.nb_slow = 2 # Number of Stations Fast and Slow currently used
        self.nb_fast = 2
        self.pmax_fast = 22
        self.pmax_slow = 3
        self.cmax = 40*4 # Maximal capacity of the CS when the 4 slots are used
        self.depart = {"slow" : np.array([self.horizon-1,self.horizon-1]), "fast" : np.array([self.horizon-1,self.horizon-1])} # Time of departure of every cars, initialize at the end of the day
        self.arrival = {"slow" : np.array([self.horizon-1,self.horizon-1]), "fast" : np.array([self.horizon-1,self.horizon-1])} # Time of arrival of every cars, initialize at the end of the day
        self.here = {"slow" : np.ones(2), "fast" : np.ones(2)}
        self.imbalance={"purchase_cover":[], "sale_cover": []}
        self.pmax_station = 40
        self.p_station = 0

    def take_decision(self, time):
        #Exemple : simple politics
        load_battery = {"fast" : np.zeros(2),"slow" : np.zeros(2)}
        #if time<6*2:
        #    load_battery = {"fast" : 17*np.ones(2),"slow" : 3*np.ones(2)}
            #From 0 am to 6 am we charge as fast as we can
        #if time>18*2:
        #    load_battery = {"fast" : -17*np.ones(2),"slow" : -3*np.ones(2)}
            #From 6 pm to 12pm we sell the stock we have
        # TO BE COMPLETED
        # Be carefull if the sum in load_battery is over pmax_station = 40 then the cars wont be charged as you want.
        # Have to return load_battery to put in update_batterie_stock to get the load.
        # load_battery must be in the following format : {"fast" : [load_car_fast_1,load_car_fast_2],"slow" : [load_car_slow_1,load_car_slow_2]}
        return load_battery

    def update_battery_stock(self,time,load_battery):

        self.nb_cars(time) # We check what cars is here

        p_max = {"slow" : [3*self.here["slow"][0],3*self.here["slow"][1]], "fast" : [22*self.here["fast"][0],22*self.here["fast"][1]]}

        c_max = {"slow" : [40*self.here["slow"][0],40*self.here["slow"][1]], "fast" : [40*self.here["fast"][0],40*self.here["fast"][1]]}

        # p_max and c_max depend on whether the car is here or not.
        self.p_station = 0
        for speed in ["slow","fast"] :
            for i in range(2):
                if abs(load_battery[speed][i]) > p_max[speed][i]:
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
                if abs(load_battery[speed][i]) > p_max[speed][i]:
                    load_battery[speed][i] = p_max[speed][i]*np.sign(load_battery[speed][i])
            # Can't put more power than p_max
                self.p_station += load_battery[speed][i]
                if self.p_station > self.pmax_station:
                    load_battery[speed][i]-= self.p_station - self.pmax_station
                    self.p_station = self.pmax_station
            #Can't put more power than the station can take : pmax_station = 40
        for speed in ["slow","fast"] :
            for i in range(2):
                if self.here[speed][i]==0:
                    new_stock[speed][i]=self.battery_stock[speed][time][i]
                if time == self.arrival[speed][i]:
                    if self.battery_stock[speed][time][i]>4:
                        new_stock[speed][i] = self.battery_stock[speed][time][i]-4
                    else :
                        new_stock[speed][i] = 0
                    # When the cars comes back it has lost 4 kWh in the battery
                self.battery_stock[speed][time+1][i]=new_stock[speed][i]
            # Update of batteries stocks
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
                if time == self.depart[speed][i] and self.battery_stock[speed][time][i]/40 < 0.25:
                    self.bill[time]+=5
        # If at the departure time of the veicule its battery isn't charged at least at 25% then you pay a 5e fine

    def compute_load(self,time,data):

        for i in range(4):   #the players discovers in live if the car is leaving or returning in the station
            if data["departures"][i]==1 and i<2:
                self.depart["slow"][i]=time
            if data["departures"][i]==1 and i>1:
                self.depart["fast"][i-2]=time

            if data["arrivals"][i]==1 and i<2:
                self.arrival["slow"][i]=time
            if data["arrivals"][i]==1 and i>1:
                self.arrival["fast"][i-2]=time

        load_battery = self.take_decision(time) # How you charge or discharge is the players choice
        load = self.update_battery_stock(time, load_battery)
        for i in range(2):
            self.load[time] += load["slow"][i] + load["fast"][i]
        self.penalty(time)
        return self.load[time]


    def observe(self, time, data, price, imbalance):

        self.prices["purchase"].append(price["purchase"])
        self.prices["sale"].append(price["sale"])

        self.imbalance["purchase_cover"].append(imbalance["purchase_cover"])
        self.imbalance["sale_cover"].append(imbalance["sale_cover"])


    def reset(self):
        self.bill = np.zeros(self.horizon)
        self.load = np.zeros(self.horizon)
        self.load_battery_periode = {"fast" : np.zeros((self.horizon,2)),"slow" : np.zeros((self.horizon,2))}

        last_bat = {"slow": self.battery_stock["slow"][-1,:], "fast": self.battery_stock["fast"][-1,:]}
        self.battery_stock = {"slow" : np.zeros((self.horizon+1,2)), "fast" : np.zeros((self.horizon+1,2))}
        self.battery_stock["slow"][0] = last_bat["slow"]
        self.battery_stock["fast"][0] = last_bat["fast"]


        self.nb_slow = 2
        self.nb_fast = 2
        self.here = {"slow" : np.ones(2), "fast" : np.ones(2)}
        self.depart = {"slow" : np.array([self.horizon-1,self.horizon-1]), "fast" : np.array([self.horizon-1,self.horizon-1])}
        self.arrival = {"slow" : np.array([self.horizon-1,self.horizon-1]), "fast" : np.array([self.horizon-1,self.horizon-1])}
        self.prices = {"purchase" : [],"sale" : []}
        self.imbalance={"purchase_cover":[], "sale_cover": []}
        self.p_station = 0



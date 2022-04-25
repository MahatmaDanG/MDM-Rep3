# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 22:37:04 2022

@author: elias
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import random as r
import matplotlib.pyplot as plt
import csv


Investment_0 = 1000                       # The initial investment in pounds
Stock_0 = 10                            # The initial price of a stock
Stability = 0.5                         # The probability of a stock increasing in one simulation cycle, 1 being guaranteed increase
Volatility_Control = 0.005               # Value that controls how much the stock can vary each cycle
DividendPercent = 0.05                    # The value of dividend as a percentage of the stock price
time = 17520

DividendCompare = DividendPercent - 0.03


def StocksOwned(I,ISP):
    Owned = I/ISP
    return(Owned) 

def StockSim(Stability, Volatility_Control, Stock_t, perception):
    stability_change = perception/50
    Stability += stability_change
    # print("stability:",Stability)
    Volatility = r.random()*Volatility_Control       # Uses a random variable and a controlled waiting to control stock varition
    StockRand = r.random()                           # Chooses whether stock increases or decreases
    Stock_change = Stock_t * Volatility
    #print('change in price: ', Stock_change)
    if StockRand < Stability:           
        Stock_t += Stock_change
    elif StockRand > Stability:
        Stock_t -= Stock_change 
    return(Stock_t)
    
    
def GraphPlot(H,V,num):
    plt.plot(H,V)
    plt.title('Value of Investment Vs Time')
    plt.xlabel('Hour(s)')
    plt.ylabel('Value of Investment')
    plt.savefig("Plots/" + str(num) +".png")
    plt.show()
    
def numericalDifferentiation(data_list): # differentiating discrete data
    if len(data_list) < 2:
        return 0
    differential = (data_list[-1] - data_list[-2]) #Assuming a time interval of 1
    #print(differential)
    return differential

def numericalIntegration(data_list): # integrating discrete data
    if len(data_list) < 2:
        return 0
    
    integral = (data_list[-2] + data_list[-1])/2 # Assuming a time interval of 1

    return integral

######### publicPerception Function Constants ############
dividendConstant = 0.5
sharePriceConstant = 0.03
changeInSharePriceConstant = 8

##########################################################
def publicPerception(div, Value, perception_t_list, dividendConstant, sharePriceConstant, changeInSharePriceConstant):
    overallSharePriceChange = (Value[-1] - Investment_0)/ Investment_0
    recentSharePriceChange = numericalDifferentiation(Value) / Investment_0
    perception_t = dividendConstant * div + sharePriceConstant * overallSharePriceChange +recentSharePriceChange * changeInSharePriceConstant # equation for change in opinion
    print("D:", dividendConstant * DividendCompare)
    print("P", sharePriceConstant * overallSharePriceChange)
    print("C",  recentSharePriceChange * changeInSharePriceConstant)
    #print(str(Value))
    perception_t_list.append(perception_t) #A list is needed to integrate back over time
    
    return (perception_t_list)

def VariableSaving(Variables):
    with open("Variable.csv","r+") as File:
        
        
        lastLine = File.readlines()[-1]
        lastLine = lastLine.split(",")
        CycleNum = int(lastLine[1])+1
        print(CycleNum)
        
        
        #print(Variables)
        Variables = (str(item)for item in Variables)
        
        VariableList = ",".join(Variables)
        print(VariableList)
        VariableList = ["\n",str(CycleNum),VariableList]
        VariableList = ",".join(VariableList)
        File.write(VariableList)
        File.close
    return(CycleNum)

Hours = [0]
Value = [Investment_0]    
perception_t_list = []
Stock_t = Stock_0
No_Owned = StocksOwned(Investment_0, Stock_0)
Dividend_t = 0
    
CycleNumber = VariableSaving((Investment_0,Stock_0,Stability,Volatility_Control,DividendPercent, dividendConstant, sharePriceConstant, changeInSharePriceConstant))

# Note 17520 is the number of hours in 2 (365 day) years

for loop in range(time):                        # The total amount of minutes simulated
    
    perception_t_list = publicPerception(DividendPercent, Value, perception_t_list, dividendConstant, sharePriceConstant, changeInSharePriceConstant) #Produces a perception value using dividends, stock value and change in stock value
    perception = numericalIntegration(perception_t_list) # integrate to find a value
    Stock_t = StockSim(Stability, Volatility_Control, Stock_t, perception)
    if loop%2190 == 0 and loop != 0 :
        Dividend_t += DividendPercent * Stock_t
    Investment_t = No_Owned*(Stock_t + Dividend_t)
    Hours.append(loop)
    Value.append(Investment_t)



GraphPlot(Hours, Value, CycleNumber)
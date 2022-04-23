# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 21:06:51 2022

@author: Mahatma
"""
import random as r
import matplotlib.pyplot as plt
import csv


Investment_0 = 1001                     # The initial investment in pounds
Stock_0 = 10                            # The initial price of a stock
Stability = 0.5                         # The probability of a stock increasing in one simulation cycle, 1 being guaranteed increase
Volatility_Control = 0.005               # Value that controls how much the stock can vary each cycle
DividendPercent = 0.01                  # The value of dividend as a percentage of the stock price


######### publicPerception Function Constants ############
dividendConstant = 0.01
sharePriceConstant = 0.000000001
changeInSharePriceConstant = 0.000001
##########################################################

def StocksOwned(I,ISP):
    Owned = I/ISP
    return(Owned) 

def StockSim(Stability, Volatility_Control, Stock_t, perception):
    Volatility = r.random()*Volatility_Control       # Uses a random variable and a controlled waiting to control stock varition
    StockRand = r.random()                           # Chooses whether stock increases or decreases
    Stock_change = Stock_t * Volatility
    #print('change in price: ', Stock_change)
    if StockRand < Stability:           
        Stock_t += Stock_change + perception 
    elif StockRand > Stability:
        Stock_t -= Stock_change + perception 
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
    #print('total:', total)
    return integral

def publicPerception(div, SO_list, perception_t_list, dividendConstant, sharePriceConstant, changeInSharePriceConstant):

    perception_t = dividendConstant * div + sharePriceConstant * SO_list[-1] + numericalDifferentiation(SO_list) * changeInSharePriceConstant # equation for change in opinion
    
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

    
CycleNumber = VariableSaving((Investment_0,Stock_0,Stability,Volatility_Control,DividendPercent, dividendConstant, sharePriceConstant, changeInSharePriceConstant))

# Note 17520 is the number of hours in 2 (365 day) years

for loop in range(17520):                        # The total amount of minutes simulated
    Dividend_t = 0
    perception_t_list = publicPerception(DividendPercent, Value, perception_t_list, dividendConstant, sharePriceConstant, changeInSharePriceConstant) #Produces a perception value using dividends, stock value and change in stock value
    perception = numericalIntegration(perception_t_list) # integrate to find a value
    Stock_t = StockSim(Stability, Volatility_Control, Stock_t, perception)
    if loop%2190 == 0:
        Dividend_t = DividendPercent * Stock_t
    Investment_t = No_Owned*(Stock_t + Dividend_t)
    Hours.append(loop)
    Value.append(Investment_t)



GraphPlot(Hours, Value, CycleNumber)
    
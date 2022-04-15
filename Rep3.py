# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 21:06:51 2022

@author: Mahatma
"""
import random as r
import matplotlib.pyplot as plt


Investment = 50                         # The initial investment in pounds
I_Stock_Price = 5                       # The initial price of a stock
Stability = 0.5                         # The odds of a stock increasing in one simulation cycle, 1 being guaranteed increae
Severity_Control = 0.01                 # Control for how much the stock can vary each cycle
DividendPercent = 0.01                  # Fine tuning for the impact of dividend


def StocksOwned(I,ISP):
    Owned = I/ISP
    return(Owned) 

def StockSim(RO,SO,Price,perception):
    Severity = r.random()*SO            # Uses a random variable and a controlled waiting to control stock varition
    StockRand = r.random()              # Chooses whether stock increases or decreases
    price_t = Price*Severity*perception
    if StockRand < Stability:           
        Price += price_t
    elif StockRand > Stability:
        Price -= price_t
    return(Price)
    
    
def GraphPlot(M,V):
    plt.plot(M,V)
    plt.title('Value of Investment Vs Minute')
    plt.xlabel('Minute')
    plt.ylabel('Value of Investment')
    plt.show()
    
def numericalDifferentiation(data_list): # differentiating discrete data
    if len(data_list) < 2:
        return 0
    differential = (data_list[-1] - data_list[-2]) #Assuming a time interval of 1
    #print(differential)
    return differential

def numericalIntegration(dataList): # integrating discrete data
    total = 0
    if len(dataList) == 0:
        total = 0
    elif len(dataList) == 1:
        total = dataList[0]
    else:
        for i in range(len(dataList)-1):
            total = total + (dataList[i] + dataList[i+1]/2) # Assuming a time interval of 1
    #print('total:', total)
    return total

def publicPerception(div, SO_list, perception_t_list):
    dividendsConstant = 0.00005
    sharePriceConstant = 0.00002
    changeInSharePriceConstant = 0.00001

    publicPerception_t = dividendsConstant * div + sharePriceConstant * SO_list[-1] + numericalDifferentiation(SO_list) * changeInSharePriceConstant # equation for change in opinion
    
    perception_t_list.append(publicPerception_t) #A list is needed to integrate back over time
    
    return perception_t_list


Minutes = [0]
Value = [Investment]    
perception_t_list = []
Vs_t = I_Stock_Price
No_Owned = StocksOwned(Investment, I_Stock_Price)

for loop in range(10000):                        # The total amount of minutes simulated
    perception_t_list = publicPerception(DividendPercent, Value, perception_t_list) #Produces a perception value using dividends, stock value and change in stock value
    perception = numericalIntegration(perception_t_list) # integrate to find a value
    Vs_t = StockSim(Stability, Severity_Control, Vs_t, perception)
    Dividend_at_t = DividendPercent * Vs_t
    Vi_t = No_Owned*(Vs_t + Dividend_at_t)
    Minutes.append(loop)
    Value.append(Vi_t)
GraphPlot(Minutes, Value)
    

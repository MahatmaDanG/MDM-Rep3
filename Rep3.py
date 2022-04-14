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

def StockSim(RO,SO,Price):
    Severity = r.random()*SO            # Uses a random variable and a controlled waiting to control stock varition
    StockRand = r.random()              # Chooses whether stock increases or decreases
    
    if StockRand < Stability:           
        Price += Price*Severity
    elif StockRand > Stability:
        Price -= Price*Severity
    return(Price)
    
    
def GraphPlot(M,V):
    plt.plot(M,V)
    plt.title('Value of Investment Vs Minute')
    plt.xlabel('Minute')
    plt.ylabel('Value of Investment')
    plt.show()


Minutes = []
Value = []    

Vs_t = I_Stock_Price
No_Owned = StocksOwned(Investment, I_Stock_Price)

for loop in range(100000):                        # The total amount of minutes simulated
    Vs_t = StockSim(Stability, Severity_Control, Vs_t)
    Dividend_at_t = DividendPercent * Vs_t
    Vi_t = No_Owned*(Vs_t + Dividend_at_t)
    Minutes.append(loop)
    Value.append(Vi_t)
GraphPlot(Minutes, Value)
    
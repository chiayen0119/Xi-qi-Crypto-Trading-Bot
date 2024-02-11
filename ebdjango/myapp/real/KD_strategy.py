import sys,datetime,numpy
import pandas as pd
import plotly
import time
import csv
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from stockstats import StockDataFrame
from real.all_api_endpoints import *


class KDClass():
    def __init__(self,start):
        self.Autotrade = start

    def stop(self):
        self.Autotrade = 'stop'


    def KD1(self,Email, API_key, API_secret):
        #定義績效
        TotalProfit=[0]
        MDD=0
        TotalTradetime=[]
        DD=[] 
        DDP=[]
        wincount=0
        count=0 
        buy=[]
        sell=[]
        buyprice=[]
        sellprice=[]
        rolling_max = 0
        rolling_min = 0
        K = 50
        D = 50
        LastK = 50
        LastD = 50
        RSV = 50
        Price = []
                
        cnt = 0
        while (cnt < 9 and self.Autotrade == 'start'):
            time.sleep(1)
            Price.append(get_ticker(Email, API_key, API_secret))
            rolling_max = max(Price)
            rolling_min = min(Price)
            LastK = K
            LastD = D
            with open('real.csv','a',newline='') as fd:
                writer = csv.writer(fd)
                writer.writerow(['Collecting data...'])
            
            print('waiting...')
            if(rolling_max == rolling_min):
                continue
            RSV = 100 * float((Price[-1] - rolling_min)/(rolling_max - rolling_min)) 
            K = 2.0/3.0 * LastK + 1.0/3.0 * RSV        
            D = 2.0/3.0 * LastD + 1.0/3.0 * K
            cnt += 1
            

        pos=0  #初始為為持有部位
        count = 0;

        while(self.Autotrade == 'start'):  
            print("LastK=", LastK, "; LastD=", LastD, "; K=", K, "; D=", D)
            with open('real.csv','a',newline='') as fd:
                writer = csv.writer(fd)
                writer.writerow(["LastK=", LastK, "; LastD=", LastD, "; K=", K, "; D=", D])
            CoverTime=datetime.datetime.now()
            #多單出場
            if pos==1: #若持有多頭部位
                if LastK >= LastD and K < D :
                    create_order(Email, API_key, API_secret, 'SELL')
                    
                    count += 1;
                    
                    CoverPrice=Price[-1]
                    pos=0
                    
                    count+=1
                    sell.append(CoverTime)
                    sellprice.append(CoverPrice)
                    Profit=CoverPrice-OrderPrice
                    TotalTradetime+=[CoverTime]
                    TotalProfit+=[TotalProfit[-1]+Profit]
                    ddnow=(TotalProfit[-1]-max(TotalProfit[1:]))
                    ddpc=ddnow/max(TotalProfit[1:])*100
                    if  ddnow <= 0:
                        DD+=[ddnow]
                        DDP+=[ddpc]
                    
                    else:
                        DD+=[0]
                        DDP+=[0]
                    if  Profit > 0:
                        wincount+=1
                else:
                    print("No transaction occured this round")
                    print("Time : ", CoverTime)
                    with open('real.csv','a',newline='') as fd:
                        writer = csv.writer(fd)
                        writer.writerow(["No transaction occured this round "+str(CoverTime)])
                    

            else: #未持有部位 pos == 0
            #多單進場
                if  LastK <= LastD and K > D:  
                    create_order(Email, API_key, API_secret, 'BUY')
                    count += 1;
                    pos=1
                    OrderTime=datetime.datetime.now()
                    OrderPrice=Price[-1]
                    buy.append(OrderTime)
                    buyprice.append(OrderPrice)
                else:
                    print("No transaction occured this round")
                    print("Time : ", CoverTime)
                    with open('real.csv','a',newline='') as fd:
                        writer = csv.writer(fd)
                        writer.writerow(["No transaction occured this round "+str(CoverTime)])

            Price.append(get_ticker(Email, API_key, API_secret))
            Price = Price[1:]
            rolling_max = max(Price)
            rolling_min = min(Price)
            if(rolling_max == rolling_min):
                time.sleep(10)
                continue
            LastK = K
            LastD = D
            RSV = 100 * float((Price[-1] - rolling_min)/(rolling_max - rolling_min)) 
            K = 2.0/3.0 * LastK + 1.0/3.0 * RSV        
            D = 2.0/3.0 * LastD + 1.0/3.0 * K       

            time.sleep(1)

            return ('tranding stop')     

        
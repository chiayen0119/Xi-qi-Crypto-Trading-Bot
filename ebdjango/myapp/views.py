from django.shortcuts import render
from django.http import HttpResponse
from backtest1.MA_RSI import MA_RSI
from backtest1.BBands import BBands
from real.KD_strategy import KDClass

from backtest1.KD_strategy import KD
import sys,datetime,numpy
import pandas as pd
from stockstats import StockDataFrame
import time
import json
import csv
a=KDClass('start')

def realweb(request):
    return render(request,'index3.html',{})
    
def pylinkweb(request):
                return render(request,'index.html',{})
def deposits(request):
                return render(request,'index2.html',{})
def result(request):
        #處理接收資料
        d1= str(request.GET['date1'])
        d2= str(request.GET['date2'])
        currency= str(request.GET['currency'])
        resolution= str(request.GET['resolution'])
        date1=int(time.mktime(time.strptime(d1, '%Y-%m-%d')))
        date2=int(time.mktime(time.strptime(d2, '%Y-%m-%d')))
        strategy= str(request.GET['strategy'])
        startequity=int(request.GET['startequity'])
     

        #策略選擇
        if strategy=='MA_RSI':
                a,b,c,fv= MA_RSI(date1,date2,currency,resolution,startequity)
        if strategy=='BBands':
                a,b,c,fv= BBands(date1,date2,currency,resolution,startequity)
        if strategy=='KD':
                a,b,c,fv= KD(date1,date2,currency,resolution,startequity)         
        g={}
        g['per']=a
        g['trade']=b
        g['score']=c
        g['abc']=fv
                
        return HttpResponse(json.dumps(g),content_type="application/json")

def realresult(request):
        email= str(request.GET['Email'])
        API_key= str(request.GET['API_key'])
        API_secret= str(request.GET['API_secret'])
        print(email)
        print(API_key)
        print(API_secret)

        global a
        a=KDClass('start')
        a.KD1(email,API_key,API_secret)

        return HttpResponse("trading stop")

def realstop(request):
        a.stop()
        return HttpResponse("trading stop")


def postreal(request):
        with open('real.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            last =list(csv_reader)[-1][-1]
        
        return HttpResponse(str(last))
        

        


        
        
        





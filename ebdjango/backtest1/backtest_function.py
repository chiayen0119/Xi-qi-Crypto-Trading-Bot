import requests
import datetime
import sys
import numpy

def GetHistoryData(date1,date2,currency,resolution):
    #api網址
    currencys_url = 'https://api.bitopro.com/v2/trading-history/'+str(currency)+'?resolution='+str(resolution)+'&from='+str(date1)+'&to='+ str(date2)  #'https://api.bitopro.com/v2/trading-history/btc_twd?resolution=1h&from='+str(15)+'&to='+ str(data2)
    #爬api資料
    resp = requests.get(currencys_url)
    r_json = resp.json()
    Hdata =list(r_json['data'])
    Mdata= []
    for i in range(len(Hdata)):
        Mdata.append(list(Hdata[i].values()))
    for i in range(len(Mdata)):
        Mdata [i][0]=datetime.datetime.utcfromtimestamp(Mdata [i][0]/1000)
        for j in range(1,6):
            Mdata [i][j]=float(Mdata [i][j])
        
    return Mdata

def GetHistoryTAKbar(date1,date2,currency,resolution):
    KBar= GetHistoryData(date1,date2,currency,resolution)
    TAKBar={}
    TAKBar['time']=numpy.array([line[0] for line in KBar])
    TAKBar['open']=numpy.array([line[1] for line in KBar])
    TAKBar['high']=numpy.array([line[2] for line in KBar])
    TAKBar['low']=numpy.array([line[3] for line in KBar])
    TAKBar['close']=numpy.array([line[4] for line in KBar])
    TAKBar['volume']=numpy.array([line[5] for line in KBar])
    return TAKBar


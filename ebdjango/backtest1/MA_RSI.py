import sys,datetime,numpy
import pandas as pd
import os
import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from .backtest_function import GetHistoryTAKbar
import ffn
from stockstats import StockDataFrame

def MA_RSI(date1,date2,currency,resolution,startequity):
    #定義績效
    
    TotalProfit=[startequity]
    DD=[]
    DDP=[]
    MDD=0
    TotalTradetime=[]
    wincount=0
    count=0
    order=[]
    close=[]
    buy=[]
    sell=[]
    buyprice=[]
    profit=[]
    sellprice=[]
    #取得Talib格式K線
    TAKBar=GetHistoryTAKbar(date1,date2,currency,resolution)
    #計算MA
    dft=pd.DataFrame(TAKBar)
    stock = StockDataFrame.retype(dft)
    TAKBar['MA']=stock['close_30_sma'].values.tolist()
    TAKBar['RSI']=stock['rsi_30'].values.tolist()
    TotalTradetime+=[TAKBar['time'][0]]



    Index=0
    for i in range(1,len(TAKBar['time'])):
        price = TAKBar['close'][i]
        lastprice = TAKBar['close'][i-1]
        ma = TAKBar['MA'][i]
        lastma= TAKBar['MA'][i-1]
        rsi = TAKBar['RSI'][i]

             
        #多單出場
        if Index==1:
            #當價格向下突破MA多單出場
            if lastprice>=lastma and price<ma:
                CoverTime=TAKBar['time'][i]
                CoverPrice=price
                Index=0
            #強制收盤出場
            elif i==len(TAKBar['time'])-1:
                CoverTime=TAKBar['time'][i]
                CoverPrice=price
                Index=0
            if Index==0:
                count+=1
                sell.append(CoverTime)
                sellprice.append(CoverPrice)
                Profit=(CoverPrice-OrderPrice)*Orderamount
                profit+=[Profit]
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
                #print('Buy Ordertime', OrderTime,'Order price', OrderPrice,'CoverTime',CoverTime, 'CoverPrice',CoverPrice,'Profit',Profit)

       
        
        #當RSI >50 且向上突破MA進場做多
        if rsi>50 and lastprice<=lastma and price>ma:
            Index=1
            OrderTime=TAKBar['time'][i]
            OrderPrice=price
            buy.append(OrderTime)
            buyprice.append(OrderPrice)
            Orderamount=startequity/price
            


    df_ffn=pd.DataFrame(TotalProfit,index=TotalTradetime,columns=['績效表現'])
    
   
    equityreturn=[]
    for i in range(len(TotalProfit)):
        equityreturn+=[((TotalProfit[i]-startequity)/startequity)*100]
    dd='{:.2%}'.format(wincount/count)
    MDD=round(min(DDP),3)
    delta= TAKBar['time'][-1]-TAKBar['time'][0]
    ye=(equityreturn[-1])/(1/(delta.days/365))
    stats = df_ffn.calc_stats()
    x=stats.stats
    r=['總報酬率','CAGR','最大回檔','Calmar ','YTD','夏普比率(Sharp)',
       '索丁諾比率(Sortino)','最佳月報酬率','最差月酬率','勝率','最佳單筆交易','最差單筆交易','交易次數']
    m=[]
    for i in range(0,45):
        if i == 3 or i == 4 or i == 5 or i == 6 or i == 7 or i == 24 or i == 25 or i == 30 or i == 31:
            m.append(str(round(x.iloc[i,0]*100,2))+'%')
    m.append(str(dd))
    m.append(round(max(profit),2))
    m.append(round(min(profit),2))
    m.append(str(count))
    dfx=pd.DataFrame(m,index=r,columns=['績效表現'])
    html=dfx.to_html()

   #plotly combined equity chart
    fig = make_subplots(rows=3, cols=1,
                        specs=[
                            [{'rowspan': 2}],
                            [None],
                            [{"secondary_y": True}]],
                            shared_xaxes=True,
                            vertical_spacing=0.02)
    

    fig.add_trace(go.Scatter(
                        x =TotalTradetime,
                        y =equityreturn,
                        name='equity',
                        line = dict(color = ('rgb(22, 96, 167)'))),
                   row=1, col=1
                   )
    fig.add_trace(go.Scatter(
                    x=TotalTradetime,
                    y=DDP,
                    name='DD%',
                    line=dict(color='rgb(250,21,25)'),
                    ),
                    row=3, col=1,
                    
                   )



    fig['layout'].update(autosize=True,
                             
                             legend=dict(orientation="h"),
                      title_text='均線策略績效表現',
                             titlefont=dict(size=24),
                             margin=go.layout.Margin(
                                 l=0,
                                 r=0,

                                 )
                             )
    
    perf_chart = plotly.offline.plot(fig,include_plotlyjs=False,output_type='div')


    #第二張圖
    trace3=go.Scatter(
                    x=TAKBar['time'],
                    y=TAKBar['MA'],
                    name='均線',
                    line=dict(color='rgb(21,21,250)'),
                    )
    
    trace8=go.Scatter(
                    x=TAKBar['time'],
                    y=TAKBar['close'],
                    name='比特幣價格線',
                    line=dict(color='rgb(250,21,21)'),
                    )
    trace9=go.Scatter(
                    x=buy,
                    y=buyprice,
                    name='買入時間',
                    marker=dict(color='rgb(21,200,21)'),
                    mode="markers"
                    )
    trace10=go.Scatter(
                    x=sell,
                    y=sellprice,
                    name='賣出時間',
                    marker=dict(color='orange'),
                    mode="markers"
                    )
    

    layout = go.Layout(
                             autosize=True,
                             legend=dict(orientation="h"),
                             title='均線策略進出場時點',
                             titlefont=dict(size=24),
                             margin=go.layout.Margin(
                                 l=0,
                                 r=0,

                                 )
                             )


    perf_chart2 = plotly.offline.plot({"data": [trace3,trace8,trace9,trace10],
                                     "layout": layout}, include_plotlyjs=False,
                                         output_type='div')        

        
    
    
    return(perf_chart,perf_chart2,html,'總利潤: '+str(round(TotalProfit[-1]-startequity,2))+'     年化報酬率'+str(round(ye*100,3))+'%     勝率: '+str(dd)+'     交易次數: '+str(count)+'     最大回檔: '+str(MDD)+'%')

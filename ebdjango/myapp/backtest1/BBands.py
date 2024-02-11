import sys,datetime,numpy
import pandas as pd
import os
import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from .backtest_function import GetHistoryTAKbar
import ffn

def BBands(date1,date2,currency,resolution,startequity):
    #定義績效
    
    TotalProfit=[startequity]
    MDD=0
    DD=[]
    TotalTradetime=[]
    DDP=[]
    wincount=0
    count=0
    order=[]
    close=[]
    orderprice=[]
    closeprice=[]
    profit=[]
    
    #取得Talib格式K線
    TAKBar=GetHistoryTAKbar(date1,date2,currency,resolution)
    dft=pd.DataFrame(TAKBar)
    rolling_mean = dft['close'].rolling(30).mean()
    rolling_std = dft['close'].rolling(30).std()
    #計算兩標準差布林線
    TAKBar['upper2']=rolling_mean+(rolling_std*2)
    TAKBar['lower2']=rolling_mean-(rolling_std*2)
    #計算一標準差布林線
    TAKBar['upper1']=rolling_mean+(rolling_std)
    TAKBar['middle1']=rolling_mean
    TAKBar['lower1']=rolling_mean-(rolling_std)
    TotalTradetime+=[TAKBar['time'][0]]

    #回測判斷
    pos=0  #初始為為持有部位

    #取得回測判斷價格
    for i in range(len(TAKBar['time'])):
        #取得本期價格
        Price = TAKBar['close'][i]
        #取得本期的兩標準差布林線
        Upper1 = TAKBar['upper1'][i]
        Lower1 = TAKBar['lower1'][i]
        #取得本期的一標準差布林線
        Upper2 = TAKBar['upper2'][i]
        Lower2 = TAKBar['lower2'][i]
        
        
              
        #多單出場
        if pos==1: #若持有多頭部位
            if  Price >= Upper1:  #價格大於兩標準差的上布林線
                CoverTime=TAKBar['time'][i]
                CoverPrice=Price
                pos=0

            #強制收盤出場
            elif i==len(TAKBar['time'])-1:
                CoverTime=TAKBar['time'][i]
                CoverPrice=Price
                pos=0


            #紀錄績效
            if  pos==0:
                count+=1
                order.append(OrderTime)
                close.append(CoverTime)
                orderprice.append(OrderPrice)
                closeprice.append(CoverPrice)
                Profit=(CoverPrice-OrderPrice)*Orderamount
                profit+=[Profit]
                TotalTradetime+=[CoverTime]
                TotalProfit+=[float(TotalProfit[-1]+Profit)]
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

        
        if pos==0: #未持有部位
        #多單進場
            if  Price <= Lower2:  
                pos=1
                OrderTime=TAKBar['time'][i]
                OrderPrice=Price
                Orderamount=startequity/Price

       

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
                        name='累積報酬率',
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
                      title_text='布林通道績效表現',
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
                    y=TAKBar['upper1'],
                    name='+1標準差',
                    line=dict(color='rgb(21,21,250)'),
                    )
    trace4=go.Scatter(
                    x=TAKBar['time'],
                    y=TAKBar['upper2'],
                    name='+2標準差',
                     line=dict(color='rgb(21,21,250)'),
                    )
    trace5=go.Scatter(
                    x=TAKBar['time'],
                    y=TAKBar['lower1'],
                    name='-1標準差',
                    line=dict(color='rgb(21,21,250)'),
                    )
    trace6=go.Scatter(
                    x=TAKBar['time'],
                    y=TAKBar['lower2'],
                    name='-2標準差',
                    line=dict(color='rgb(21,21,250)'),
                    )
    trace7=go.Scatter(
                    x=TAKBar['time'],
                    y=TAKBar['middle1'],
                    name='均線',
                    line=dict(color='black'),
                    )
    trace8=go.Scatter(
                    x=TAKBar['time'],
                    y=TAKBar['close'],
                    name='比特幣價格線',
                    line=dict(color='rgb(250,21,21)'),
                    )
    trace9=go.Scatter(
                    x=close,
                    y=closeprice,
                    name='出場時間',
                    marker=dict(size=10,color='rgb(21,200,21)'),
                    mode="markers"
                    )
    trace10=go.Scatter(
                    x=order,
                    y=orderprice,
                    name='進場時間',
                    marker=dict(size=10,color='orange'),
                    mode="markers"
                    )
       
    layout = go.Layout(
                             autosize=True,
                             legend=dict(orientation="h"),
                             title='布林通道進出場時點',
                             titlefont=dict(size=24),
                             margin=go.layout.Margin(
                                 l=0,
                                 r=0,

                                 )
                             )



    perf_chart2 = plotly.offline.plot({"data": [trace3,trace4,trace5,trace6,trace7,trace8,trace9,trace10],
                                     "layout": layout}, include_plotlyjs=False,
                                         output_type='div')        
    
    
    return(perf_chart[5:-6],perf_chart2[5:-6],html,'總利潤: '+str(round(TotalProfit[-1]-startequity,2))+'     年化報酬率'+str(round(ye*100,3))+'%     勝率: '+str(dd)+'     交易次數: '+str(count)+'     最大回檔: '+str(MDD)+'%')



















            
            
        
        
        

        


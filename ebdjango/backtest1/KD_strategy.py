import sys,datetime,numpy
import pandas as pd
import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from .backtest_function import GetHistoryTAKbar
from stockstats import StockDataFrame

def KD(date1,date2,currency,resolution,startequity):
    #定義績效
    TotalProfit=[startequity]
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
    profit=[]


    #取得Talib格式K線
    TAKBar=GetHistoryTAKbar(date1,date2,currency,resolution)
    dft=pd.DataFrame(TAKBar)
    stock = StockDataFrame.retype(dft)
    TAKBar['K']=stock['kdjk'].values.tolist()
    TAKBar['D']=stock['kdjd'].values.tolist()
    TotalTradetime+=[TAKBar['time'][0]]
    
    #回測判斷
    pos=0  #初始為為持有部位

    #取得回測判斷價格
    for i in range(1,len(TAKBar['time'])):

        #取得本期價格
        Price = TAKBar['close'][i]
        K = TAKBar['K'][i]
        D = TAKBar['D'][i]
        LastK = TAKBar['K'][i-1]
        LastD = TAKBar['D'][i-1]
              
        #多單出場
        if pos==1: #若持有多頭部位
            if (LastK >= LastD and K < D) or (i==len(TAKBar['time'])-1):
                CoverTime=TAKBar['time'][i]
                CoverPrice=Price
                pos=0
                
            if pos==0:
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

        
        if pos==0: #未持有部位
        #多單進場
            if  LastK <= LastD and K > D:  
                pos=1
                OrderTime=TAKBar['time'][i]
                OrderPrice=Price
                buy.append(OrderTime)
                buyprice.append(OrderPrice)
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
                      title_text='KD策略績效表現',
                             titlefont=dict(size=24),
                             margin=go.layout.Margin(
                                 l=0,
                                 r=0,

                                 )
                             )
    
    
    perf_chart = plotly.offline.plot(fig,include_plotlyjs=False,output_type='div')

    #第二張圖
    fig2 = make_subplots(rows=3, cols=1,
                        specs=[
                            [{'rowspan': 2}],
                            [None],
                            [{}]],
                            shared_xaxes=True,
                            vertical_spacing=0.02)
    trace1=go.Scatter(
                    x=TAKBar['time'],
                    y=TAKBar['close'],
                    name='比特幣價格線',
                    line=dict(color='rgb(0,0,0)'))
     
     
    trace3=go.Scatter(
                    x=TAKBar['time'],
                    y=TAKBar['K'],
                    name='K9',
                    line=dict(color='rgb(250,21,210)'),
                    )
    
    trace8=go.Scatter(
                    x=TAKBar['time'],
                    y=TAKBar['D'],
                    name='D9',
                    line=dict(color='rgb(21,21,250)'),
                    )
    trace9=go.Scatter(
                    x=buy,
                    y=buyprice,
                    name='買進時間',
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
                    
    fig2.append_trace(trace1,1,1)
    fig2.append_trace(trace10,1,1)
    fig2.append_trace(trace9,1,1)
    fig2.append_trace(trace3,3,1)
    fig2.append_trace(trace8,3,1)
                    
    
    fig2['layout'].update(autosize=True,
                        title_text='KD策略進出場點',
                        legend=dict(orientation="h"),
                        titlefont=dict(size=24),
                        margin=go.layout.Margin(
                                 l=0,
                                 r=0,

                                 )
                              )
    
                              

    perf_chart2 = plotly.offline.plot(fig2,include_plotlyjs=False,output_type='div')        

        


    return(perf_chart,perf_chart2,html,'總利潤: '+str(round(TotalProfit[-1]-startequity,2))+'     年化報酬率'+str(round(ye*100,3))+'%     勝率: '+str(dd)+'     交易次數: '+str(count)+'     最大回檔: '+str(MDD)+'%')

            



        
            
    

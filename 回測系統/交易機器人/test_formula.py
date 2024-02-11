import pandas as pd
import matplotlib.pyplot as plt
import xlsxwriter

#MA計算
def MA(s,l,df):
    df['ma_s'] = df.iloc[:,1].rolling(s).mean() #以收盤價計算s日均線
    df['ma_l'] = df.iloc[:,1].rolling(l).mean() #以收盤價計算l日均線
    df['ma_sign'] = 0 #MA交易訊號
    #黃金交叉訊號1
    df['ma_sign'][(df['ma_s'].shift(1) < df['ma_l'].shift(1)) & (df['ma_s'] >= df['ma_l'])]=1
    #死亡交叉訊號-1
    df['ma_sign'][(df['ma_s'].shift(1) > df['ma_l'].shift(1)) & (df['ma_s'] <= df['ma_l'])]=-1


#出場函數
def outp(df,r,b,price,i):
    r=r+b*df.iloc[i,price]
    df['ret'].iloc[i]=r
    r=0
    b=0
    return(r,b)

#進場函數
def inp(df,r,b,i):
    df['sign'].iloc[i]=b
    r=r-b*df.iloc[i,4]
    return(r,b)

#當日結算與停損
def stoploss(df,loss,r,b,i):
    cpl= r+b*df.iloc[i,4] #當日結算current profit and loss
    cplr= cpl/(-b*r) #當日結算/進場成本current profit and loss ratio
    if cplr<loss:
        (r,b)=outp(df,r,b,4,i+1) #符合停損條件，以下一筆開盤價出場
    return(r,b)
        
#計算策略績效指標
def result_F(cost,count,df):
    last=df['cus'].iloc[-1] #計算最後報酬 
    ROI= last/cost
    def maxdrawdown(s):
        s=s.cummax()-s
        return(s.max())
    mdd=maxdrawdown(df['cus'])
    if count ==0:
        w=0
    else:
        w=df['ret'][df['ret']>0].count()/count

    #製成表格
    result = pd.DataFrame({
        '初始投入':[cost],
        '最後報酬':[last],
        '交易次數':[count],
        '最大回損':[mdd],
        '勝率':[w],
        '累積投資報酬率':[ROI]})
    return(result)

#輸出回測資料
def out_excel(name,df,result,K,L):
    writer=pd.ExcelWriter(name+'.xlsx')
    df.to_excel(writer,'0')
    result.to_excel(writer,'result')
    df['cus'].to_excel(writer,'result',startcol=7)
    workbook=writer.book
    chart = workbook.add_chart({'type':'line'})
    chart.add_series({'values':'=result!$I$'+str(K+1)+':$I$'+str(L+1),'name':'cus'})
    worksheet=writer.sheets['result']
    worksheet.insert_chart('J2',chart)
    writer.save()



    
    

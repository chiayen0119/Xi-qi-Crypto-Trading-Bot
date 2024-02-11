from test_formula import *
df=pd.read_csv('test.csv',encoding='BIG5')
MA(24,48,df)

#進行買賣計算
K=2
L=len(df) #紀錄資料長度
r=0 #初始交易金流量
b=0 #設定多空方，多方1、空方-1、未持有0
df['sign']=0 #紀錄進場
df['ret']=0 #紀錄出場結算
count=0

for i in range(K-1,L):
    if i < L-1:
        if b==1:
            #若死亡交叉
            if df['ma_sign'].iloc[i]==-1:
                (r,b)=outp(df,r,b,4,i+1) #下一筆開盤價多方出場
        if b==0:
            #若為黃金交叉
             if df['ma_sign'].iloc[i]==1:
                 (r,b)=inp(df,r,1,i+1)
                 count=count+1
                 if count==1:
                     cost=df.iloc[i,4]
        if b!=0:
            #設停損點
            (r,b)=stoploss(df,-0.03,r,b,i)
            
    elif i==L-1:
        if b!=0:
            (r,b)=outp(df,r,b,1,i)
        
#計算累積損益
df['cus']=df['ret'].cumsum()
df['cus'].plot()
result=result_F(cost,count,df)
out_excel('stl',df,result,K,L)
                 

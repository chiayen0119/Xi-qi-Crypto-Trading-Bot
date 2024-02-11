import requests
import time

BASE_URL = 'https://www.bitopro.com/'
now = int(time.time())
currencys_url = 'https://api.bitopro.com/v2/trading-history/btc_twd?resolution=1h&from='+str(now-31556926)+'&to='+ str(now)

import datetime
timeStamp = 1381419600
dateArray = datetime.datetime.utcfromtimestamp(timeStamp)
otherStyleTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")

import requests
resp = requests.get(currencys_url)
# print(resp)
# print(resp.status_code)
# print(resp.json())
r_json = resp.json()

import csv
import pandas as pd
pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
resp_json = resp.json()
data_list = resp_json['data']


# for data in data_list:
#     print(data)

df = pd.DataFrame(data_list)
print(df)
df.to_csv("test.csv")

#!/usr/bin/env python3
from real.client import Client
import pandas as pd
import time
import csv


def get_ticker(Email, API_key, API_secret):
    client = Client(Email, API_key, API_secret)
    result = client.get_public_all_tickers("btc_twd")
    return float(pd.DataFrame(result).data[2])

def create_order(Email, API_key, API_secret, action):
    client = Client(Email, API_key, API_secret)
    result = client.get_public_all_tickers("btc_twd")
    result2 = client.get_private_account_balance()
    if(action == 'BUY'):
        amount = round(float(pd.DataFrame(result2).data[0]['available'])/float(str(pd.DataFrame(result).data[2])), 3)
        print("amount:",amount)
        #print("amount = ", amount)
        if(amount < 0.0025):
            print("Not enough money")
            with open('real.csv','a',newline='') as fd:
                    writer = csv.writer(fd)
                    writer.writerow(["Not enough money"])
            return
        result1 = client.set_private_create_order('btc_twd', action, str(amount), str(pd.DataFrame(result).data[2]))
        #print(f"[I] Invoked set_private_create_order API Result: \n    {result}\n")
        print("You have bought ", amount, " bitcoin.")
        with open('real.csv','a',newline='') as fd:
                    writer = csv.writer(fd)
                    writer.writerow(["You have bought "+ str(amount)+ " bitcoin."])
        
    else:
        amount = round(float(pd.DataFrame(result2).data[1]['available']), 3)
        #print("amount = ", amount)
        if(amount < 0.0025):
            print("Not enough money")
            with open('real.csv','a',newline='') as fd:
                    writer = csv.writer(fd)
                    writer.writerow(["Not enough money"])
            return 
        result1 = client.set_private_create_order('btc_twd', action, str(amount), str(pd.DataFrame(result).data[2]))
        print("You have sold ", amount, "bitcoin.")
        with open('real.csv','a',newline='') as fd:
                    writer = csv.writer(fd)
                    writer.writerow(["You have sold "+ str(amount)+ " bitcoin."])
        
        
            

# if __name__ == '__main__':
#     client = Client('b06701216@ntu.edu.tw', '14640ce6b1140cba29ea9d0690c2f08d', '$2a$12$cGk4jpczxLf/jsvXTWJHYeUIgqknL2OWWugn9hPYgqxHCscAc.hbO')
    

#     try:
#             # Public (Read)
#         result = client.get_public_all_tickers("btc_twd")
#             # 创建excel文件  
#         row = 0
#         # while True:
#         #     df = pd.DataFrame(result)
            
#         #     time.sleep(1)
#         #     row += 1

#         #     print("每秒即時價格:",df.data[2])
#         #     if row == 1:
#         #         break

            
#         #print("df:",df)
#         #print(f"[I] Invoked get_public_all_tickers() API Result: \n    {result}\n")
#         #result = client.get_public_available_currencies()
#         #print(f"[I] Invoked get_public_available_currencies() API Result: \n    {result}\n")
#         #result = client.get_public_available_pairs()
#         #print(f"[I] Invoked get_public_available_pairs() API Result: \n    {result}\n")
#         #result = client.get_public_order_book('btc_twd', 10)
#         #print(f"[I] Invoked get_public_order_book('btc_twd', 10) API Result: \n    {result}\n")
#         #result = client.get_public_recent_trades('btc_twd')
#         #print(f"[I] Invoked get_public_recent_trades('btc_twd') API Result: \n    {result}\n")r

#         # Private (Read)
        
#         #result = client.set_private_create_order('btc_twd', 'BUY', str(0.0025), str(213000))
#         #print(f"[I] Invoked set_private_create_order('btc_twd', 'BUY', 0.0025, 213000)API Result: \n    {result}\n")

#         result = client.get_private_account_balance()
#         amount = pd.DataFrame(result).data[0]['available']
#         print("amount :", amount)

#         print(f"[I] Invoked get_private_account_balance() API Result: \n    {result}\n")
#         #result = client.get_private_order_data('btc_twd', 12345678)
#         #print(f"[I] Invoked get_private_order_data('btc_twd', 12345678) API Result: \n    {result}\n")
#         #result = client.get_private_order_history()
#         #print(f"[I] Invoked get_private_order_history() API Result: \n    {result}\n")
#         #result = client.get_private_order_list('btc_twd', 1, False)
#         #print(f"[I] Invoked get_private_order_list('btc_twd', 1, False) API Result: \n    {result}\n")



#         # Private (Write)
#         # result = client.set_private_cancel_order('btc_twd', 12345678)
#         # print(f"[I] Invoked set_private_cancel_order('btc_twd', 12345678) API Result: \n    {result}\n")

        


# except Exception as error:
#     print(f"[X] {str(error)}")

#     # Networking errors occurred here
#     response = getattr(error, 'read', None)
#     if callable(response):
#         print(f"[X] {response().decode('utf-8')}")

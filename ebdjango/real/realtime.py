from real.KD_strategy import *
from real.all_api_endpoints import *
#from bband import *
import time

try:

	if __name__ == '__main__':
		# Email = input("Please enter Email : ")
		# API_key = input("Please enter API_key : ")
		# API_secret = input("Please enter API_secret : ")
		#print("now:", datetime.datetime.now())
		KD("b06701216@ntu.edu.tw", "14640ce6b1140cba29ea9d0690c2f08d", "$2a$12$cGk4jpczxLf/jsvXTWJHYeUIgqknL2OWWugn9hPYgqxHCscAc.hbO")
		#BBands("b06701216@ntu.edu.tw", "14640ce6b1140cba29ea9d0690c2f08d", "$2a$12$cGk4jpczxLf/jsvXTWJHYeUIgqknL2OWWugn9hPYgqxHCscAc.hbO")
		#print(get_ticker("b06701216@ntu.edu.tw", "14640ce6b1140cba29ea9d0690c2f08d", "$2a$12$cGk4jpczxLf/jsvXTWJHYeUIgqknL2OWWugn9hPYgqxHCscAc.hbO"))
		#create_order("b06701216@ntu.edu.tw", "14640ce6b1140cba29ea9d0690c2f08d", "$2a$12$cGk4jpczxLf/jsvXTWJHYeUIgqknL2OWWugn9hPYgqxHCscAc.hbO", "BUY")

except Exception as error:
	print(f"[X] {str(error)}")


	# Networking errors occurred here
	response = getattr(error, 'read', None)
	if callable(response):
	    print(f"[X] {response().decode('utf-8')}")
		
"""
Pretio_Server_Pinger.py

Parameters:
None

Author: Brian Holden
Date: Dec 4 2019
Usage: Run python file. will connect to server, get JSON, process and export to SCV file.
"""

import json
import requests
import time 
import csv

api_bearer = "LpNe5bB4CZnvkWaTV9Hv7Cd37JqpcMNF"			# bearer token for server
api_url= "https://atlas.pretio.in/atlas/coding_quiz"	# server address

headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {0}'.format(api_bearer)}

"""Pings the server, if sucessful, returns parsed JSON, otherwise returns error code"""
def ping():
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return response.status_code

"""Used for sort, converts payout field to a float to handle decimal values"""
def myFunc(e):
    return float(e["payout"])

def main():
    output = ping()
    """if server gives status code of 429, wait 60 seconds and retry"""
    if (output == 429):
        time.sleep(60)
        main()
        """if server gives status code of 500, leave message and terminate"""
    elif (output == 500):
        print("Server status: 500, shutting down")
        """Succesful return of parced JSON"""
    elif (type(output) is  dict):
        print("Server contacted succesfully")
        with open("offers.csv", mode="w", encoding="utf-8", newline='') as csv_file: 	#encoding important for being able to handle non english characters
            fieldnames = ["active", "cap", "name", "payout", "platform"]				#CSV file collumns, matches JSON structure 
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for (k, v)in output.items():
                v.sort(reverse=True, key=myFunc)
                for l in v:
                    writer.writerow(l)
    else:
        print("Server code error: " + output)
main()
print("Ping complete")
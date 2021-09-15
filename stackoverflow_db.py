import mysql.connector
from datetime import date
import pandas as pd
from pandas.io import json
import requests
from pprint import pprint
from types import SimpleNamespace

from requests.api import delete

mydb = mysql.connector.connect(host='localhost',
                               user='root',
                               password='',
                               database='recruiter') 

if mydb.is_connected():
    print("connected")

#mydb.close()

username = "tapati93"
# url = f"https://api.stackexchange.com/2.3/users/{636656}/answers?order=desc&sort=activity&site=stackoverflow"
url = f"https://api.stackexchange.com/2.3/users?pagesize=100&order=desc&sort=reputation&site=stackoverflow"
#url = f"https://api.github.com/users/{username}"
user_data = requests.get(url).json()

#print(user_data)

mycursor = mydb.cursor()

sql = ("delete from stackoverflow_details")
mycursor.execute(sql)

mydb.commit()

# mycursor.close()
# mydb.close()

sql = ("INSERT INTO stackoverflow_details (Acc_id, User_Name, Gold_count, Silver_Count, Bronze_count, Reputation, Stack_overflow_link, Accept_rate) \
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")           
#VALUES (%d, %s, %d, %d, %d, %d, %s)")

Acc_id = []
User_Name = []
Location = []
Gold_count = []
Silver_Count = []
Bronze_count = []
Accept_rate = []
Reputation = []
stack_overflow_link = []

for item in user_data['items']:

    #Github_link = []
    #bc_dataaa = item['accept_rate']
    Acc_id.append(item['account_id'])
    User_Name.append(item['display_name'])
    #Location.append(item['location'])
    Gold_count.append(item['badge_counts']['gold'])
    Silver_Count.append(item['badge_counts']['silver'])
    Bronze_count.append(item['badge_counts']['bronze'])
    #Accept_rate.append(item['accept_rate'])
    Reputation.append(item['reputation'])
    stack_overflow_link.append(item['link'])
    accept_rate = None
    if 'accept_rate' in item:
        accept_rate = item['accept_rate']
    

    val = [(item['account_id'], item['display_name'], item['badge_counts']['gold'], item['badge_counts']['silver'], item['badge_counts']['bronze'],
                            item['reputation'], item['link'], accept_rate)]
    mycursor.executemany(sql, val)
    #bc_dataaa = item['badge_counts']
    #print(bc_dataaa)

#mycursor.executemany(sql, val)

mydb.commit()

print("Records Inserted")

mycursor.close()
mydb.close()
# for item in Acc_id:
#     print(item)

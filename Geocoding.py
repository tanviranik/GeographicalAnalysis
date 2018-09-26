from sqlalchemy import create_engine
import urllib3
import requests
import json
import time
import pandas as pd
import csv


df = pd.read_csv('Product Weekly Sales_AUG2018_Partial.csv')

writer = open("CustomerSales_3.csv", 'a')
writer.write('Ship to name|Ship to Address|Ship to City|Ship to State|Ship to Zip|Record Owner|Order Date|Item Description|Invoice Amount|Total Shipped|Contract Price|Latitude|Longitude\n')


for index, row in df.iterrows():
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + row['Ship to Address'].strip() + ',' + row['Ship to City'].strip() + ',' + row['Ship to State'].strip() + '&key=AIzaSyDsuzNnJrvwFhot_ciZ7wkArQmHCj38ZaI'
    response = requests.get(url)
    data = json.loads(response.text)
    if data['status'] == 'OK':
        lat = data['results'][0]['geometry']['location']['lat']
        lng = data['results'][0]['geometry']['location']['lng']
        print(row['Ship to Address'].strip() + ',' + row['Ship to City'].strip() + ',' + row['Ship to State'].strip() + ': ' + str(lat) + ',' + str(lng))
        line = row['Ship to name'].strip() + '|' + row['Ship to Address'].strip() + '|' + row['Ship to City'].strip() + '|' + row['Ship to State'].strip() + '|' + row['Ship to Zip'].strip() + '|' + row['Record Owner'].strip() + '|' + row['Order Date'].strip() + '|' + row['Item Description'].strip() + '|' + str(row['Invoice Amount']).strip().replace("$", "")+ '|' + str(row['Total Shipped']).strip()+ '|' + str(row['Contract Price']).strip().replace("$", "") + '|' + str(lat) + '|' + str(lng) + '\n'
    else: 
        line = row['Ship to name'].strip() + '|' + row['Ship to Address'].strip() + '|' + row['Ship to City'].strip() + '|' + row['Ship to State'].strip() + '|' + row['Ship to Zip'].strip() + '|' + row['Record Owner'].strip() + '|' + row['Order Date'].strip() + '|' + row['Item Description'].strip() + '|' + str(row['Invoice Amount']).strip().replace("$", "")+ '|' + str(row['Total Shipped']).strip()+ '|' + str(row['Contract Price']).strip().replace("$", "") + '|' + '-10000000' + '|' + '10000000' + '\n'
    writer.write(line)

writer.close()

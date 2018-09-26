from sqlalchemy import create_engine
import urllib3
import requests
import json
import time

engine = create_engine("mssql+pymssql://sa:dataport@192.168.100.61/GroupDashboard")
query = "SELECT distinct \
                            [Latitude] \
                            ,[Longitude]  \
                           FROM [dbo].[viewGPSUpdate] where Latitude is not null and Longitude is not null and Latitude != 0 and Longitude != 0  order by 1"

#truncateTableQuery = "truncate table [HygieneDashboard].[dbo].[DistributorLatLonAddressGOOGLEMAP]"
#engine.execute(truncateTableQuery)

for row in engine.execute(query):
    try:
        url = "http://dev.virtualearth.net/REST/v1/Locations/"+str(row.Latitude)+","+str(row.Longitude)+"?o=json&key=AskJODvnAZC1nI8MHds9-wZlaC205kv8gFrjnYH_oxQF0kPWlryfkNT3EAugpLMq";
        #url = "http://maps.googleapis.com/maps/api/geocode/json?latlng=" + str(row.Lat) + ","+str(row.Lon)+"&sensor=true"
        response = requests.get(url)
        pages = json.loads(response.text)
        #address = pages['results'][0]['formatted_address']
        address = pages['resourceSets'][0]['resources'][0]['address']['formattedAddress']
        #print(address)
        print(str(row.Latitude), str(row.Longitude), str(address))
        #insertTableQuery = "Insert into  [dbo].[CreditTrackingCustLocation] Values(%f,%f,N'%s')" %(float(row.Latitude), float(row.Longitude), address.replace("'", r"\'"))
        insertTableQuery = "Insert into  [dbo].[CreditTrackingCustLocation] Values(" + str(row.Latitude) + "," + str(row.Longitude) + ",'" +  address.replace("'", r"\'") + "')"
        engine.execute(insertTableQuery)
    except:
        print("Address Not Found")
        insertTableQuery = "Insert into  [dbo].[CreditTrackingCustLocation] Values(" + str(row.Latitude) + "," + str(row.Longitude) + ",'Address Not Found')"
        engine.execute(insertTableQuery)
    time.sleep(0.01)

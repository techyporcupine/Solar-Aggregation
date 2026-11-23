# Solar Data Aggregation

import requests
import json
import pandas
from datetime import date, datetime, timedelta
import io

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

todayDate = date.today().strftime("%Y-%m-%d") # today's date

def satcon():
    global totalDCPower
    satconPayload = {
        "binSize": 5,
        "context": "site",
        "start": todayDate,
        "end": todayDate,
        "sectionCode": -1,
        "query": None,
        "chartType": 15,
        "source": ["S45602"]
    }
    satconURL = 'https://pubdisplay.alsoenergy.com/api/view/chart?lastChanged=1900-01-01T00:00:00.000Z'
    satconRawJSON = json.dumps(satconPayload)
    satconHeaders = {"Content-Type": "application/json", "Referer": 'https://pubdisplay.alsoenergy.com/kiosk/18014398509527586?dashkey=2a5669734965572f4141773d3d&tag=8802171'}

    try:
        response = requests.post(satconURL, data=satconRawJSON, headers=satconHeaders, timeout=20) # send post request to alsoenergy
    except requests.exceptions.RequestException as e:
        print(f"Error grabbing Hartzler data: {e}")
        return


    satconInverterACData = response.json()['series'][1] # select the first list under 'series'
    satconInverterACOutput = satconInverterACData['dataBinned']
    satconInverterACOutputClean = [x for x in satconInverterACData['dataBinned'] if x is not None] # removes all entries with "None" in them
    satconCurrentACkW = satconInverterACOutputClean[-1]

    satconInverterDCData = response.json()['series'][0] # select the first list under 'series'
    satconInverterDCOutput = satconInverterDCData['dataBinned']
    satconInverterDCOutputClean = [x for x in satconInverterDCData['dataBinned'] if x is not None] # removes all entries with "None" in them
    satconCurrentDCkW = satconInverterDCOutputClean[-1]
    
    #print(satconInverterDCOutputClean)

    hours = [i * 5 / 60 for i in range(len(satconInverterACOutputClean))]

    plt.plot(hours, satconInverterACOutputClean)
    plt.xlabel("Hour of day")
    plt.ylabel("Array AC output (kW)")
    plt.xticks(range(0, 25, 1))
    plt.yticks(range(0, 105, 5))
    plt.show()

    #print("----Sadie Hartzler Library Solar----")
    #print("Producing since November 2010")
    #print("Latest data:")
    #print("- AC Wattage: " + str(satconCurrentACkW) + "kW")
    #print("- DC Wattage: " + str(satconCurrentDCkW) + "kW")

satcon()
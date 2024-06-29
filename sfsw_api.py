import databasse_insertings as dbInsert
import requests
import datetime
import re

def getStationListBasics():
    start = dbInsert.getDatetimeNow()
    response = requests.post("https://sfws.lfrz.at/json.php", params={"command":"getstations"})
    end = dbInsert.getDatetimeNow()
    callId = dbInsert.saveCallData("getstations", "{}", start, end)

    return response.json(), callId

def getStationDetails(stationCode):
    start = dbInsert.getDatetimeNow()
    response = requests.post("https://sfws.lfrz.at/json.php", params={"command":"getstation", "stationcode":stationCode})
    end = dbInsert.getDatetimeNow()
    callId = dbInsert.saveCallData("getstation", "{stationcode: " + stationCode + "}", start, end)

    return response.json(), callId

def getCurrentRadiation():
    start = dbInsert.getDatetimeNow()
    response = requests.post("https://sfws.lfrz.at/json.php", params={"command":"getdata", "maxid":"0"})
    end = dbInsert.getDatetimeNow()
    callId = dbInsert.saveCallData("getdata", "{maxid: 0}", start, end)

    return response.json()['values'], callId


def getStationsLastXDaysRadiation(stationCode, x):
    start = dbInsert.getDatetimeNow()
    # if not re.search("^AT", stationCode):
    #     stationCode = 
    
    response = requests.post("https://sfws.lfrz.at/json.php", params={"command":"getstationdata", "stationcode":stationCode, "a":x, "b":"0"})
    end = dbInsert.getDatetimeNow()
    callId = dbInsert.saveCallData("getdata", "{maxid: 0}", start, end)
    return response.json()['v'], callId
import database_init as databaseInit
import databasse_insertings as db_insert
import sfsw_api as sfws

def intToRgbString(value):
    # Extract Colors
    red = (value >> 16) & 0xFF
    green = (value >> 8) & 0xFF
    blue = value & 0xFF

    return f"RGB({red},{green},{blue})"

def intToHexString(value):
    # Extract Colors
    red = (value >> 16) & 0xFF
    green = (value >> 8) & 0xFF
    blue = value & 0xFF

    return f"#{red:02X}{green:02X}{blue:02X}"

def stationCodeToId(stationCode):
    connection = databaseInit.openDBConn()
    cursor = connection.cursor()

    stationList = cursor.execute("SELECT id, station_code FROM stations").fetchall()
    connection.close()
    for number, string in stationList:
        # Prüfe, ob der String dem Zielstring entspricht
        if string == stationCode:
            return number

def saveStations():
    basicjson, callId = sfws.getStationListBasics()
    db_insert.saveStationListBasics(basicjson, callId)
    for stationCode, stationData in basicjson.items():
        advancedjson, callId = sfws.getStationDetails(stationCode)
        db_insert.saveStationDetails(advancedjson, callId)

def saveCurrentRadiation():
    datajson, callId = sfws.getCurrentRadiation()
    db_insert.saveCurrentRadiation(datajson, callId)

def saveStationsLastXDaysRadiation(stationCode, x):
    datajson, callId = sfws.getStationsLastXDaysRadiation(stationCode, x)
    db_insert.saveStationsLastXDaysRadiation(datajson, callId, stationCode)

def saveAllStationsLastXDaysRadiation(x):
    connection = databaseInit.openDBConn()
    cursor = connection.cursor()

    stationList = cursor.execute("SELECT id, station_code FROM stations").fetchall()
    for stationId, stationCode in stationList:
        datajson, callId = sfws.getStationsLastXDaysRadiation(stationCode, x)
        db_insert.saveStationsLastXDaysRadiation(datajson, callId, stationCode)
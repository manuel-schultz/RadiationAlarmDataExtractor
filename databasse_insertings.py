import database_init as db
import grabdata
import datetime
import uuid

def getDatetimeNow():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def timestampToDate(timestamp):
    dt = datetime.datetime.utcfromtimestamp(timestamp)
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def saveCallData(action, parameters, start, end):
    connection = db.openDBConn()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO api_calls (call_action, call_parameters, started_at, ended_at) VALUES (?, ?, ?, ?)", (action, parameters, start, end))
    id = cursor.lastrowid
    connection.commit()
    db.closeDBConn(connection)
    return id

def saveStationListBasics(json, callId):
    connection = db.openDBConn()
    cursor = connection.cursor()

    for station_code, station_data in json.items():
        cursor.execute("SELECT id FROM stations WHERE station_code = ?", (station_code,))
        existing_entry = cursor.fetchone()
        if existing_entry:
            cursor.execute("UPDATE stations SET api_call_id = ?,german_name = ?, img_coordinates_x = ?, img_coordinates_y = ?, updated_at = ? WHERE station_code = ?", (
                callId,
                station_data['n'], 
                station_data['x'], 
                station_data['y'], 
                getDatetimeNow(), 
                station_code
            ))
        else:
            cursor.execute("""INSERT INTO stations 
                           (api_call_id, station_code, station_code_country, station_code_number, german_name, img_coordinates_x, img_coordinates_y, created_at, updated_at)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
                callId,
                station_code,
                station_code[:2],
                int(station_code[2:]),
                station_data['n'],
                station_data['x'],
                station_data['y'],
                getDatetimeNow(),
                getDatetimeNow()
            ))
    connection.commit()
    connection.close()

def saveStationDetails(json, callId):
    connection = db.openDBConn()
    cursor = connection.cursor()
    cursor.execute("UPDATE stations SET api_call_id = ?, geo_coordinates_latitude = ?, geo_coordinates_longitude = ?, geo_coordinates_elevation = ?, updated_at = ? WHERE station_code = ?", (
        callId,
        json['la'], 
        json['lo'], 
        json['el'], 
        getDatetimeNow(), 
        json['c']
    ))
    connection.commit()
    connection.close()

def saveCurrentRadiation(json, callId):
    connection = db.openDBConn()
    cursor = connection.cursor()
    for stationCode, radiationData in json.items():
        stationId = grabdata.stationCodeToId(stationCode)
        cursor.execute("SELECT id FROM radiation_levels WHERE station_id = ? AND measured_timestamp = ?", (str(stationId), radiationData['d']))
        existing_entry = cursor.fetchone()
        if not existing_entry:    
            cursor.execute("""INSERT INTO radiation_levels 
                           (uuid, api_call_id, station_id, measured_at, measured_timestamp, measured_radiation_value, rgb_color, hex_color, created_at, updated_at)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
                str(uuid.uuid4()),
                str(callId),
                str(stationId),
                timestampToDate(radiationData['d']),
                str(radiationData['d']),
                str(radiationData['v']),
                grabdata.intToRgbString(radiationData['c']),
                grabdata.intToHexString(radiationData['c']),
                getDatetimeNow(),
                getDatetimeNow()
            ))
    connection.commit()
    connection.close()

def saveStationsLastXDaysRadiation(json, callId, stationCode):
    connection = db.openDBConn()
    cursor = connection.cursor()
    timestamps = [str(item['d']) for item in json]
    timestamplist = ",".join(timestamps)
    stationId = grabdata.stationCodeToId(stationCode)
    placeholders = ','.join('?' * len(timestamps))

    existingResults = cursor.execute(f"SELECT * FROM radiation_levels WHERE station_id = ? AND measured_timestamp IN ({placeholders})", (
        [str(stationId)] + timestamps
    ))
    existingTimestamps = {row[5] for row in existingResults.fetchall()}
    filteredJSON = [entry for entry in json if entry['d'] not in existingTimestamps]

    if len(filteredJSON) <= 0:
        return

    valueSets = []
    for values in filteredJSON:
        valueSets.append(f"""("{str(uuid.uuid4())}", {str(callId)}, {str(stationId)}, "{timestampToDate(values['d'])}", "{str(values['d'])}", {str(values['v'])}, "{grabdata.intToRgbString(values['c'])}", "{grabdata.intToHexString(values['c'])}", "{getDatetimeNow()}", "{getDatetimeNow()}")""")

    valueSetsString = ",".join(valueSets)
    cursor.execute(f"INSERT INTO radiation_levels (uuid, api_call_id, station_id, measured_at, measured_timestamp, measured_radiation_value, rgb_color, hex_color, created_at, updated_at) VALUES {valueSetsString}")

    connection.commit()
    connection.close()
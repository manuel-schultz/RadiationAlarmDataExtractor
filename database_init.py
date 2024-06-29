import sqlite3 as sql
import sys
import re
from os import listdir
from os.path import isfile, join

def databaseLocation():
    return "sql/RadiationsDB.sqlite3"

def migrationLocation():
    return "sql/migrations"

def filterIsMigrationFileName(filename):
    return re.search("^\d{4}-.+\.sql$", filename)

def openDBConn():
    connection = sql.connect(databaseLocation())
    return connection

def closeDBConn(connection):
    connection.close()

def executeMigrations():
    # get all migration files
    migrations = [f for f in listdir(migrationLocation()) if isfile(join(migrationLocation(), f))]
    migrations = list(filter(filterIsMigrationFileName, migrations))
    
    connection = openDBConn()
    cursor = connection.cursor()

    with open(join(migrationLocation(), migrations[0]), 'r') as sqlFile:
        schemaScript = sqlFile.read()
    cursor.executescript(schemaScript)

    migrationVersions = cursor.execute("SELECT migration_version FROM schema_histories")
    migrationVersionArray = []
    for row in migrationVersions.fetchall():
        migrationVersionArray.append(row[0])
   

    for migrationFileName in migrations:
        migrationNumber = int(migrationFileName.split("-")[0])
        if migrationNumber not in migrationVersionArray:
            with open(join(migrationLocation(), migrationFileName), 'r') as sqlFile:
                migrationScript = sqlFile.read()
            cursor.executescript(migrationScript)
    print('INFO: Migrations up-to-date')

    closeDBConn(connection)

def displayDBEntryAmounts():
    connection = openDBConn()
    cursor = connection.cursor()
    apiCallAmount = str(cursor.execute("SELECT COUNT(id) FROM api_calls;").fetchone()[0])
    stationAmount = str(cursor.execute("SELECT COUNT(id) FROM stations;").fetchone()[0])
    radiationLevelAmount = str(cursor.execute("SELECT COUNT(id) FROM radiation_levels;").fetchone()[0])

    numberLength = max(len(apiCallAmount), len(stationAmount), len(radiationLevelAmount))

    print("You have the following amount of entries in your Database:")
    print(f" - api_calls:          {' ' * (numberLength - len(apiCallAmount))}[{apiCallAmount}]")
    print(f" - stations:           {' ' * (numberLength - len(stationAmount))}[{stationAmount}]")
    print(f" - radiation_levels:   {' ' * (numberLength - len(radiationLevelAmount))}[{radiationLevelAmount}]")

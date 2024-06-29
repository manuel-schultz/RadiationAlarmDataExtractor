import database_init as databaseInit
import databasse_insertings as dbInsert
import sfsw_api as sfws
import grabdata

print("INFO: Program started at: " + dbInsert.getDatetimeNow())
databaseInit.executeMigrations()
print()
grabdata.saveStations()

# grabdata.saveCurrentRadiation()
grabdata.saveAllStationsLastXDaysRadiation(200)

databaseInit.displayDBEntryAmounts()




print()
print("INFO: Program closed at: " + dbInsert.getDatetimeNow())


# TODO: Timed automated requests with following Timing:
#       grabdata.saveCurrentRadiation()                     15m - 1h
#       grabdata.saveAllStationsLastXDaysRadiation(14)      7d
#       grabdara.saveStations()                             28d

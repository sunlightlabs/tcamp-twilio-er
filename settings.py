# settings for tcamp-twilio-er.py

# twilio account settings
TWLIO_ACCNT = "***REMOVED***"
TOKEN = "***REMOVED***"
TCAMP_FON = "***REMOVED***"

# settings for google ... should make this a unique APP PASSWD FIXME
GOOG_USER="timball@sunlightfoundation.com"
GOOG_PASSWD="***REMOVED***"
GOOG_SPREADSHEET_KEY="***REMOVED***"

# in our case sheets 0,1 have data and sheet 2 is a tester
if DEBUG is not True:
    SHEETS_WE_CARE_ABOUT = [0, 1]
else:
    SHEETS_WE_CARE_ABOUT = [2]
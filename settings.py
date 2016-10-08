# settings for tcamp-twilio-er.py

DEBUG = False
# twilio account settings
TWLIO_ACCNT = ""
TOKEN = ""
TCAMP_FON = ""

# settings for google ... should make this a unique APP PASSWD FIXME
GOOG_USER=""
GOOG_PASSWD=""
GOOG_SPREADSHEET_KEY=""

# in our case sheets 0,1 have data and sheet 2 is a tester
if DEBUG is not True:
    SHEETS_WE_CARE_ABOUT = [0, 1]
else:
    SHEETS_WE_CARE_ABOUT = [2]

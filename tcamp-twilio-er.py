#!/usr/bin/env python
#
# tcamp-twilio-er.py
#            --timball@sunlightfoundation.com
#
# $Id$
#

#DEBUG = False

# some setting info for twilio
try:
    import settings
except ImportError, exp:
    pass

import sys
import click

# this is a helper class to parse and de-munge all of zubies data
class zubies_contact:
    def __init__(self, csv_row):
        self.name = csv_row[0]
        self.txt_msg = csv_row[1]
        self._date_frag = csv_row[2]
        self._time_frag = csv_row[3]
        self._fon_frag = csv_row[4]
        self.fon = self._munge_fon()
        self.date_string = self._munge_date()


    def _munge_date(self):
        import time
        import datetime
        import dateutil.parser as dp

        _date_string = None
        _timestmp = None

	try:
		month,day,year = str(self._date_frag).split('/')
		self._date_frag = "%s-%s-%s" % (year, month.zfill(2), day.zfill(2))
	except:
		print "name: %s date:%s time:%s fon:%s" % (self.name, self._date_frag, self._time_frag, self._fon_frag);
		sys.exit(1)


        try:
            hour, minute, second = self._time_frag.split(':')
        except:
            sys.stderr.write("SHIT error ! |%s| |%s| |%s| |%s| |%s|" % (self.name, self.txt_msg, self.fon, self._date_frag, self._time_frag))
            hour, minute, second = "11:11:11".split(':') # just keep going
            sys.exit(1)

        if int(hour) < 6:
            # XXX arbitrarily declaring anything before 6 to be in the PM . --timball
            hour = int(hour) + 12
            hour = str(hour)
        self._time_frag = "%s:%s:%s" % (hour.zfill(2), minute.zfill(2), second.zfill(2))

        _date_string = "%s %s" % (self._date_frag, self._time_frag)
        #_timestmp = time.mktime(datetime.datetime.strptime(_date_string, "%Y-%m-%d %H:%M:%S").timetuple())

        self._date_frag = None
        self._time_frag = None

        #dp.parse(_date_string + ' ' + 'EDT')
        return _date_string

    def _munge_fon(self):
        import re
        p = re.compile(' |-')
        try:
            fon = p.sub('', self._fon_frag)
        except:
            sys.stderr.write("PANTS error ! |%s| |%s| |%s| |%s| |%s|" % (self.name, self.txt_msg, self._fon_frag, self._date_frag, self._time_frag))
            sys.exit(1)
        self._fon_frag = None
        return "+1%s" % (fon)
# ---- end class zubie ------------------------------------


def get_zubies_spreadsheet():
    import gspread

    gc = gspread.login(settings.GOOG_USER, settings.GOOG_PASSWD)
    spread = gc.open_by_key(settings.GOOG_SPREADSHEET_KEY)

    list_of_lists = []
    for i in settings.SHEETS_WE_CARE_ABOUT:
        wks = spread.get_worksheet(i)
        tmp = wks.get_all_values()
        tmp = tmp[1:] # get rid off the first line , there must be a smart way to do this FIXME
        list_of_lists = list_of_lists + tmp

    return list_of_lists


def send_sms (contact):
    from time import time
    from twilio.rest import TwilioRestClient

    if settings.DEBUG:
        print "DEBUG :: %s %s %s %s" % (time(), contact.name, contact.fon, contact.txt_msg)

    client = TwilioRestClient(settings.TWLIO_ACCNT, settings.TOKEN)
    message = client.messages.create(to=contact.fon, from_=settings.TCAMP_FON, body=contact.txt_msg)


@click.command()
def main():
    import sys
    from time import sleep
    from apscheduler.scheduler import Scheduler

    if settings.DEBUG:
        click.echo("hello")

    # create a scheduler and start it
    sched = Scheduler()
    sched.start()        # start the scheduler

    zubies_data = []
    sheet = get_zubies_spreadsheet()

    # fill zubies_data from work sheets
    for row in sheet:
        this_contact = zubies_contact(row)
        zubies_data.append(this_contact)

    # take zubies_data and put it into the scheduler
    for i in zubies_data:
        #if DEBUG:
        #    print "DEBUG :: %s %s |%s| |%s|" % (i.name, i.fon, i.date_string, i.txt_msg)
        try:
            job = sched.add_date_job(send_sms, i.date_string, [i])
            print "SCHED :: %s %s |%s| |%s|" % (i.name, i.fon, i.date_string, i.txt_msg)
        except:
            sys.stderr.write('NOT SCHED PAST EVENT :: '+i.name+' '+i.date_string+'\n')
            True # eat errors

    i = 0
    while True:
        sleep(1)
        if True:
            i += 1
            if (i % 10 == 0):
                sys.stdout.write('.'); sys.stdout.flush()
            if (i % 60 == 0):
                sys.stdout.write(' '); sys.stdout.flush()
            if (i % 120 == 0):
                sys.stdout.write('\n'); sys.stdout.flush()
                i=0


if __name__ == "__main__":
    main()

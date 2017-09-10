#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

def probable_date():
    '''uses datetime to find out if it's weekend or after 14.30 (the mensa closing time)
    returns the next date the mensa opens''' 
    weekday = datetime.datetime.today().weekday()
    todays_date=str(datetime.datetime.now()).split()[0]
    time=str(datetime.datetime.now()).split()[1]
    #weekday: 1,2,3,4,5,6,7; date: "2017-09-05"; time: "19:46:07.851512" (formatwise, not actually those numbers)
    
    # checking the daytime
    hour=int(time.split(":")[0])
    if hour <= 13:
        mensa="today_relevant"
    elif hour >= 15:
        mensa="today_irrelevant"
    elif hour == 14:
        if int(time.split(":")[1]) >=30:
            mensa="today_irrelevant"
        else:
            mensa="today_relevant"

    # checking the weekday (weekend or not)
    if weekday == 6: #if true/sunday:
        date = str(datetime.datetime.now() + datetime.timedelta(days=1)).split()[0] #today
    elif weekday == 5: #if saturday.
        date = str(datetime.datetime.now() + datetime.timedelta(days=2)).split()[0] #tomorrow
    elif weekday == 4: # if friday, checking if mensa is already closed
        if mensa == "today_relevant":
            date = todays_date
        else:
            date = str(datetime.datetime.now() + datetime.timedelta(days=3)).split()[0] #monday
    else: #mon-tue-wed-thu
        if mensa == "today_relevant":
            date = todays_date
        else:
            date = str(datetime.datetime.now() + datetime.timedelta(days=1)).split()[0] #tomorrow

    return date

def get_readable_date(mydate):
    '''function takes actual date and checks weekday
    returns name of weekdays''' 
    only_day=mydate[-2:]    
    splitted = mydate.split("-")
    year = int(splitted[0])
    month = int(splitted[1])
    day = int(splitted[2])

    # converting actual date into weekday name to transfer to the audio input
    if datetime.date(year, month, day).isoweekday() == 1:
        week_day = 'Montag' 
    elif datetime.date(year, month, day).isoweekday() == 2:
        week_day = 'Dienstag'
    elif datetime.date(year, month, day).isoweekday() == 3:
        week_day = 'Mittwoch'
    elif datetime.date(year, month, day).isoweekday() == 4:
        week_day = 'Donnerstag'
    elif datetime.date(year, month, day).isoweekday() == 5:
        week_day = 'Freitag'
    elif datetime.date(year, month, day).isoweekday() == 6:
        week_day = 'Montag'
    elif datetime.date(year, month, day).isoweekday() == 7:
        week_day = 'Montag'
        
    
    return week_day



def is_weekend(given_date):
    '''function takes given date and checks if mensa is open or not
    return boolean'''
    splitted = given_date.split("-")
    year = int(splitted[0])
    month = int(splitted[1])
    day = int(splitted[2])

    if datetime.date(year, month, day).isoweekday() == 5 or datetime.date(year, month, day).isoweekday() == 6: #wenn nach morgen /übermorgen auf sams/sonn gemapped, wird, nehmen wir besser nächsten montag
        weekend_bool=True
    else:
        weekend_bool=False
            
    return weekend_bool

    
if __name__ == '__main__':
    probable_date()
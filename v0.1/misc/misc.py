#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

def probable_date():
    #this function uses the datetime module to find out if it's the weekend or after 14.30 (the mensa closing time)
    #returns the next date the mensa opens by finding he next monday
    weekday = datetime.datetime.today().weekday()
    todays_date=str(datetime.datetime.now()).split()[0] #it'd be possible to use the today() func instead
    time=str(datetime.datetime.now()).split()[1]
    #examples: weekday: 1,2,3,4,5,6,7; date: "2017-09-05"; time: "19:46:07.851512" (formatwise, not actual numbers)
    
    # checking the current daytime
    hour=int(time.split(":")[0])
    if hour <= 13:
        mensa="today_relevant"
    elif hour >= 15:
        mensa="today_irrelevant"
    elif hour == 14:
        if int(time.split(":")[1]) >=30: #here we can check the minutes
            mensa="today_irrelevant"
        else:
            mensa="today_relevant"

    # checking the weekday (is it weekend or not?)
    if weekday == 6: #if true it's sunday:
        date = str(datetime.datetime.now() + datetime.timedelta(days=1)).split()[0] #so the probable date is the current one plus one, monday
    elif weekday == 5: #if saturday.
        date = str(datetime.datetime.now() + datetime.timedelta(days=2)).split()[0] #saturday+2=monday
    elif weekday == 4: # if friday, we first need to check if the mensa is already closed
        if mensa == "today_relevant":
            date = todays_date
        else:
            date = str(datetime.datetime.now() + datetime.timedelta(days=3)).split()[0] #monday, in three days from friday
    else: #mon-tue-wed-thu
        if mensa == "today_relevant": #if the mensa is still open on any day, the user propably wants the current day information
            date = todays_date
        else:
            date = str(datetime.datetime.now() + datetime.timedelta(days=1)).split()[0] #else, tomorrows

    return date

def get_readable_date(mydate):
    #function takes an actual date and returns a string of the respective weekday
    #the datetime func returning a number corresponding to weekdays needs year,month,and day seperated
    #only the last two number are the day, so we sort that:
    splitted = mydate.split("-")
    year = int(splitted[0])
    month = int(splitted[1])
    day = int(splitted[2])

    # converting actual date into weekday name to transfer it to the audio output in rendertemplate
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
    #function takes a given date and checks if mensa is open or not on that day, returns respective boolean
    #this function could be further improved by returning False on holidays etc.
    splitted = given_date.split("-")
    year = int(splitted[0])
    month = int(splitted[1])
    day = int(splitted[2])

    if datetime.date(year, month, day).isoweekday() == 5 or datetime.date(year, month, day).isoweekday() == 6: 
    #wenn per Angabe wie "morgen" oder "übermorgen" auf sa/so gemapped wird, nehmen wir besser nächsten Montag, um KeyErrors beim DateLookup zu verhindern
    #man könnte alternativ sagen, an diesen Tagen hat die Mensa geschlossen, aber eine positive, informative Antwort freut den Nutzer vielleicht auch
        weekend_bool=True
    else:
        weekend_bool=False
        #wenn der weekend_bool als False zurückkommt, wird das probable_date (siehe oben) als date lookup verwendet
    return weekend_bool

    
if __name__ == '__main__':
    probable_date()
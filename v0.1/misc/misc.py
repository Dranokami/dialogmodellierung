#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

def probable_date():
    #uses datetime to find out if its weekend or after 14.30 (the mensa closing time) and returns the next date an dem die mensa auf hat 
    weekday = datetime.datetime.today().weekday()
    todays_date=str(datetime.datetime.now()).split()[0]
    time=str(datetime.datetime.now()).split()[1]
    #now weekday is 1,2,3,4,5,6,7, date is "2017-09-05" and time is "19:46:07.851512" (format wise, not actually those numbers)
    

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

    ## überprüfen, ob es wochenende ist.
    if weekday == 6: #wenn es So ist:
        date = str(datetime.datetime.now() + datetime.timedelta(days=1)).split()[0] #morgen
    elif weekday == 5: # wenn es Sa ist.
        date = str(datetime.datetime.now() + datetime.timedelta(days=2)).split()[0] #übermorgen
    elif weekday == 4: # wenn es Fr ist, muss überprüft werden ob die mensa noch auf hat
        if mensa == "today_relevant":
            date = todays_date
        else:
            date = str(datetime.datetime.now() + datetime.timedelta(days=3)).split()[0] #montag
    else: #mo-di-mi-do
        if mensa == "today_relevant":
            date = todays_date
        else:
            date = str(datetime.datetime.now() + datetime.timedelta(days=1)).split()[0] #morgen

    #print date, type(date)
    return date

def get_readable_date(mydate): #readable to mo/di/mi/do/fr abstürz bei heute + vegetarisch 
    only_day=mydate[-2:]
    if only_day == "01":
        readable_date = "ersten" #am ersten
    elif only_day == "03":
        readable_date = "dritten" #am dritten
    elif only_day == "07":
        readable_date = "siebten" #am siebten
    elif only_day == "08":
        readable_date = "achten"
    elif only_day == "09":
        readable_date = "neunten" 
    elif int(only_day)<=19: 
        readable_date=only_day+"ten"
    else:
        readable_date=only_day+"sten"
    
    splitted = mydate.split("-")
    year = int(splitted[0])
    month = int(splitted[1])
    day = int(splitted[2])

    if datetime.date(year, month, day).isoweekday() == 0:
        week_day = 'Montag' 
    elif datetime.date(year, month, day).isoweekday() == 0:
        week_day = 'Dienstag'
    elif datetime.date(year, month, day).isoweekday() == 0:
        week_day = 'Mittwoch'
    elif datetime.date(year, month, day).isoweekday() == 0:
        week_day = 'Donnerstag'
    elif datetime.date(year, month, day).isoweekday() == 0:
        week_day = 'Freitag'
    elif datetime.date(year, month, day).isoweekday() == 0:
        week_day = 'Samstag'
    elif datetime.date(year, month, day).isoweekday() == 0:
        week_day = 'Sonntag'
        
    
    return (week_day, ', den ',readable_date)



def is_weekend(given_date):
    #returns True if day is weekend, false if not 
    #try: 
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
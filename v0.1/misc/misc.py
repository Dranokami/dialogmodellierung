#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

def probable_date():
    #uses datetime to find out if its weekend or after 14.30 (the mensa closing time) and returns the next date an dem die mensa aufhat 
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

def get_readable_date(mydate):
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
    else: 
        readable_date=only_day+"sten"

    return readable_date


if __name__ == '__main__':
    probable_date()
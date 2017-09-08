#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import datetime
#import web_scraper.fake_scrape as mensa
import mensa_web_scraping as mensa
import misc.misc as misc 

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


def error_handling(error):
    error_msg = render_template(error)
    return statement(error_msg)

#This py get's handles all intents, external information about food gets imported from the scraper, intented days (based on opening times) from misc function

@ask.launch

def new_game():

    food = mensa.scrape_pipeline() #get's a food dict or loading error
    if type(food) == str:
        error_handling(food)
    date = misc.probable_date() #get's probably intended date as string, based on weekday and time (if mensa is open, today, if closed tommorows or mondays date!)
    todays_date=str(datetime.datetime.now()).split()[0]
    
    maindish = food[date]["maindish"]
    veggiedish = food[date]["veggiedish"]
        
    if date == todays_date: #Wenn der heutige Tag noch relevant ist, kommt die Standard welcome msg
        welcome_msg = render_template('welcome', maindish=maindish, veggiedish=veggiedish)
    else: #wenn der tag abweichend ist, wird alternativ informiert, das die mensa zu hat
        welcome_msg = render_template('alt_welcome', maindish=maindish, veggiedish=veggiedish)

    session.attributes['food'] = food #übergibt das food attribut und relevante datum der session 
    session.attributes['date'] = date

    return question(welcome_msg)



@ask.intent("MenuIntent")

def menuoptions():
    option_msg = render_template('menu_options')
    return question(option_msg)



@ask.intent("DayIntent")

def dayoptions():
    option_msg = render_template('day_options')
    return question(option_msg)



@ask.intent("VitalIntent")

def vitalinfo():
    try: 
        food = session.attributes['food']
    except KeyError:
        food = mensa.scrape_pipeline()
        if type(food) == str:
            error_handling(food)

    todays_date=str(datetime.datetime.now()).split()[0]
    date = misc.probable_date()
    option_msg = food[date]["vital"]
    return question(option_msg)



@ask.intent("BeilagenIntent")

def beilageninfo():
    try: 
        food = session.attributes['food']
    except KeyError: #wenn die session kein food und date hat, hat man nich mit welcomegestartet und muss die info erst holen
        food = mensa.scrape_pipeline() #get's a food dict or loading error as string
        if type(food)==str:
            error_handling(food)
    
    todays_date=str(datetime.datetime.now()).split()[0]
    date = misc.probable_date() #get's probably intended date as string, based on weekday and time (if mensa is open, today, if closed tommorows or mondays date!)
    
    beilagen = food[date]["sidedish"]
    
    if date == todays_date: #Wenn der heutige Tag noch relevant ist, kommt die heutige vital msg
        option_msg = render_template('beilagen', beilagen=beilagen)
    else: #wenn der tag abweichend ist, wird alternativ informiert, das die mensa zu hat
        option_msg = render_template('alt_beilagen', beilagen=beilagen)

    return question(option_msg)



@ask.intent("WeekdayIntent", mapping={'mydate': 'Weekday'})
 
def weekday_request(mydate):
    #todo: samstag /sonntag möglich machen als slot und abfangen

    date = misc.probable_date() #get's probably intended date as string, based on weekday and time (if mensa is open, today, if closed tommorows or mondays date!)
    readable_day = misc.get_readable_date(mydate)
    
    #print "übergeben wurde", str(mydate)
    weekend_bool = misc.is_weekend(str(mydate)) #returns true if the requestet date is a weekend
    if weekend_bool == True:
        #print "und das ist ein wochenende"
        mydate = date
    
    try:
        food = session.attributes['food']
        date = session.attributes['date']
    except KeyError: #wenn die session kein food und date hat, hat man nich mit welcomegestartet und muss die info erst holen
        food = mensa.scrape_pipeline() #get's a food dict or loading error as string
        if type(food)==str:
            error_handling(food)
    
    if mydate == '': # passiert, wenn wir ohne slot ungewollt in diesen Intent gelangen:
        mydate = date #sicherheitshalbe heute/morgen datum nehmen
    maindish = food[str(mydate)]["maindish"]
    veggiedish = food[str(mydate)]["veggiedish"]

    weekday_reply=render_template('specdate', wochentag=readable_day, maindish=maindish, veggiedish=veggiedish)
    #first, check if a dialouge_sate exists:
    try:
        grounded = session.attributes['dialogue_state'] #if it exists, we save the date that was talked about here
        grounded['talked_date'] = str(mydate)           #and give it back as session attribute
        session.attributes['dialogue_state'] = grounded
    except: #wenn es keinen gibt, erstellen wir es
        grounded = {}
        grounded['talked_date'] = str(mydate) #saves what was talked about before 
        session.attributes["dialogue_state"] = grounded
    return question(weekday_reply)




@ask.intent("VeggieIntent")

def myveggie():
    try: 
        food = session.attributes['food']
    except KeyError: #wenn die session kein food und date hat, hat man nich mit welcomegestartet und muss die info erst holen
        food = mensa.scrape_pipeline() #get's a food dict or loading error as string
        if type(food)==str:
            error_handling(food)
    
    todays_date=str(datetime.datetime.now()).split()[0]
    date = misc.probable_date() #get's probably intended date as string, based on weekday and time (if mensa is open, today, if closed tommorows or mondays date!)
    
    veggiedish = food[date]["veggiedish"]

    if date == todays_date: #Wenn der heutige Tag noch relevant ist, kommt die heutige vital msg
        option_msg = render_template('veggie_msg', veggiedish=veggiedish)
    else: #wenn der tag abweichend ist, wird alternativ informiert, das die mensa zu hat
        option_msg = render_template('alt_veggie_msg', veggiedish=veggiedish)


    return question(option_msg)
   


@ask.intent("FinalIntent")  #the premade stopintents somehow triggered beilagen

def end_msg():
    goodbye = render_template('quitmsg')
    return statement(goodbye)





if __name__ == '__main__':

    app.run(debug=True)
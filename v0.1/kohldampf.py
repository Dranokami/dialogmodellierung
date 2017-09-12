#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import datetime
#import web_scraper.fake_scrape as mensa this module is used when the scraper doesn't work and includes a fake mensa plan and random pesudo errors
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
    if error != "error_03":
        return statement(error_msg)
    else: # it's possible to answer on this error, therefore it's a question statement
        return question(error_msg)

#This py handles all intents, external information about food, get's imports from the scraper, and intented days (based on opening times) from misc function

@ask.launch

def new_game():

    food = mensa.scrape_pipeline() #get's a food dict or a loading error
    if type(food) == str:
        error_handling(food)
    date = misc.probable_date() #get's probably intended date as string, based on weekday and time (if mensa is open, today, if closed, tommorows or mondays date)
    todays_date=str(datetime.datetime.now()).split()[0]#we could use today() func instead
    #next, we map the infomation we just found out to the mainmeals in the food dictionary from the webscraper:
    maindish = food[date]["maindish"]
    veggiedish = food[date]["veggiedish"]
        
    if date == todays_date: #If the current day is still relevant, the standard welcome msg will be called
        welcome_msg = render_template('welcome', maindish=maindish, veggiedish=veggiedish)
    else: # if the day is not the current date, the information that the mensa is already closed will be given
        welcome_msg = render_template('alt_welcome', maindish=maindish, veggiedish=veggiedish)

    #session.attributes['food'] = food # transfers the food attribute but not the relevant date

    return question(welcome_msg)



@ask.intent("MenuIntent")

def menuoptions(): #dieser Intent informiert über die Menümöglichkeiten, wenn ein Nutzer generische Anfragen wie "Mahlzeiten" stellt 
    option_msg = render_template('menu_options')
    return question(option_msg)



@ask.intent("DayIntent")

def dayoptions(): #dieser Intent informiert den Benutzer über die Wochentagsfunktion, falls eine generische Anfragen wie "Wochentag" gestellt wird
    option_msg = render_template('day_options')
    return question(option_msg)



@ask.intent("VitalIntent")

def vitalinfo():
    try: #dieser try/except block überprüft ob ein .json bereits in der welc.msg oder vorherigen aufrufen erstellt wurde
        food = mensa.read_json(mensa.check_json())
        dict(food)
    except: #wenn das nicht der Fall ist, wird die webscrape-pipeline gestartet, um die Mahlzeiten abzufragen
        food = mensa.scrape_pipeline()
        if type(food) == str:
            error_handling(food)

    todays_date=str(datetime.datetime.now()).split()[0] #wie in der welc.msg. und jedem Intent, werden Datumsangaben benötigt
    date = misc.probable_date()

    vitales_essen = food[date]["vital"]

    if todays_date == date: 
        option_msg = render_template('vital_msg', vital =vitales_essen)
    else: 
        option_msg = render_template('alt_vital_msg', vital = vitales_essen)

    return question(option_msg)



@ask.intent("BeilagenIntent")

def beilageninfo(): #funktioniert genau wie Vital nur mit alternativem lookup im dict nach entsprechender message
    try: 
        food = mensa.read_json(mensa.check_json())
        dict(food)
    except: #wenn die session kein 'food' hat, hat man nich mit welcome gestartet und muss die Info erst holen (zb.: frage Teufelsküche nach Beilagen)
        food = mensa.scrape_pipeline()
        if type(food)==str:
            error_handling(food)
    
    todays_date=str(datetime.datetime.now()).split()[0]
    date = misc.probable_date() #get's probably intended date as string, based on weekday and time (if mensa is open, today, if closed, tommorows or mondays date!)
    
    beilagen = food[date]["sidedish"]
    
    if date == todays_date: #Wenn der heutige Tag noch relevant ist, kommt die heutige vital msg
        option_msg = render_template('beilagen', beilagen=beilagen)
    else: #wenn der Tag abweichend ist, wird alternativ informiert, dass die Mensa zu hat
        option_msg = render_template('alt_beilagen', beilagen=beilagen)

    return question(option_msg)



@ask.intent("WeekdayIntent", mapping={'mydate': 'Weekday'})
 

def weekday_request(mydate):
    #Dieser Intent wird immer aufgerufen, wenn ein bestimmter Wochentag angegeben / angefragt wurde (wird aber leider manchmal mit leerem slot erkannt)
    date = misc.probable_date() #wie immer Datumsangaben, dieses Mal als zurückfall-Wert, falls dieser intent ohne erkanntes Datum aufgerufen wird
    
    if mydate=='': #diese if passiert, wenn wir ohne Slot ungewollt in diesen Intent gelangen
        mydate=date
    
    #readable date konvertiert das nun feststehnde Datum zu einem "readable" string (zu montag/di/mi/do/fr als string)
    readable_day = misc.get_readable_date(mydate)

    weekend_bool = misc.is_weekend(str(mydate)) #returns true if the requested date is a weekend
    if weekend_bool == True:
        #print "und das ist ein Wochenende"
        mydate = date #in dem Fall fallen wir aus das probable-default-Datum zurück, damit in jedem Fall eine informative Auskunft gegeben wird
    
    try: #ab hier funktioniert der Intent genau wie welc msg, beilagen und vital intent
        food = mensa.read_json(mensa.check_json())
        dict(food)
    except: #wenn die session kein 'food' und date hat, hat man nich mit welcomegestartet und muss die Info erst holen
        food = mensa.scrape_pipeline() #get's a food dict or loading error as string
        if type(food)==str:
            error_handling(food)

    maindish = food[str(mydate)]["maindish"]
    veggiedish = food[str(mydate)]["veggiedish"]

    weekday_reply=render_template('specdate', wochentag=readable_day, maindish=maindish, veggiedish=veggiedish)
    
    #this was an attempt at grounding, maybe we just spoke about vitalmenü, so it checks if such a dialouge_sate exists
    #also we should save the date the user is currently requesting for future queries 
    try:
        grounded = session.attributes['dialogue_state'] #if it exists, we save the date that was talked about here
        grounded['talked_date'] = str(mydate)           #and gives it back as session attribute
        session.attributes['dialogue_state'] = grounded
    except: #wenn es keinen gibt, erstellen wir es
        grounded = {}
        grounded['talked_date'] = str(mydate) #saves what was talked about before 
        session.attributes["dialogue_state"] = grounded
    #unfortunately, this isn't included in the other intents, yet 
    
    return question(weekday_reply)




@ask.intent("VeggieIntent")

def myveggie(): #works just like vital and beilage, just with the veggiemenü and voicelines
    try: 
        food = mensa.read_json(mensa.check_json())
        dict(food)
    except: #wenn die session kein food und date hat, hat man nich mit welcomegestartet und muss die info erst holen
        food = mensa.scrape_pipeline() #get's a food dict or loading error as string
        if type(food)==str:
            error_handling(food)
    
    todays_date=str(datetime.datetime.now()).split()[0]
    date = misc.probable_date() #get's probably intended date as string, based on weekday and time (if mensa is open, today, if closed tommorows or mondays date!)
    
    veggiedish = food[date]["veggiedish"]

    if date == todays_date: #Wenn der heutige Tag noch relevant ist, kommt die heutige vital msg
        option_msg = render_template('veggie_msg', veggiedish=veggiedish)
    else: #wenn der Tag abweichend ist, wird alternativ informiert, dass die Mensa zu hat
        option_msg = render_template('alt_veggie_msg', veggiedish=veggiedish)

    return question(option_msg)
   


@ask.intent("FinalIntent")  #our default good bye msg =) 

def end_msg():
    goodbye = render_template('quitmsg')
    return statement(goodbye)





if __name__ == '__main__':

    app.run(debug=True)
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
    else: #auf error drei kann man antworten bzw soll, daher wird es als question statt statement returned
        return question(error_msg)

#This py get's handles all intents, external information about food gets imported from the scraper, intented days (based on opening times) from misc function

@ask.launch

def new_game():

    food = mensa.scrape_pipeline() #get's a food dict or a loading error
    if type(food) == str:
        error_handling(food)
    date = misc.probable_date() #get's probably intended date as string, based on weekday and time (if mensa is open, today, if closed tommorows or mondays date)
    todays_date=str(datetime.datetime.now()).split()[0]#we could use today() func instead
    #next we map the dates we just found out to the mainmeals in the food dictionary from the webscraper:
    maindish = food[date]["maindish"]
    veggiedish = food[date]["veggiedish"]
        
    if date == todays_date: #Wenn der heutige Tag noch relevant ist, kommt die Standard welcome msg
        welcome_msg = render_template('welcome', maindish=maindish, veggiedish=veggiedish)
    else: #wenn der tag abweichend ist, wird alternativ informiert, das die mensa zu hat
        welcome_msg = render_template('alt_welcome', maindish=maindish, veggiedish=veggiedish)

    #session.attributes['food'] = food #übergibt das food attribut und relevante datum der session, wird nicht verwendet

    return question(welcome_msg)



@ask.intent("MenuIntent")

def menuoptions(): #dieser intent informiert über die Menü Möglichkeiten, wenn ein Nutzer generische Anfragen wie "Mahlzeiten" angibt
    option_msg = render_template('menu_options')
    return question(option_msg)



@ask.intent("DayIntent")

def dayoptions(): #dieser intent informiert den Benutzer über die Wochentags Funktion, falls eine generische Anfragen wie "Wochentag" angegeben wurde
    option_msg = render_template('day_options')
    return question(option_msg)



@ask.intent("VitalIntent")

def vitalinfo():
    try: #dieser try/except block überprüft ob ein Json bereits in der welc.msg oder vorherigen aufrufen erstellt wurde
        food = mensa.read_json(mensa.check_json())
        dict(food)
    except: #wenn das nicht der fall ist, wird die webscrape pipeline gestartet um die informationen abzufragen
        food = mensa.scrape_pipeline()
        if type(food) == str:
            error_handling(food)

    todays_date=str(datetime.datetime.now()).split()[0] #wie in der welc.msg. und jedem intent, werden Datumsangaben benötigt
    date = misc.probable_date()

    vitales_essen = food[date]["vital"]

    if todays_date == date: 
        option_msg = render_template('vital_msg', vital =vitales_essen)
    else: 
        option_msg = render_template('alt_vital_msg', vital = vitales_essen)

    return question(option_msg)



@ask.intent("BeilagenIntent")

def beilageninfo(): #funktioniert genau wie Vital nur mit alternativem lookup im dict nud entsprechender message
    try: 
        food = mensa.read_json(mensa.check_json())
        dict(food)
    except: #wenn die session kein food hat, hat man nich mit welcomegestartet und muss die info erst holen (zb.: frage teufelsküche nach Beilagen)
        food = mensa.scrape_pipeline()
        if type(food)==str:
            error_handling(food)
    
    todays_date=str(datetime.datetime.now()).split()[0]
    date = misc.probable_date() #get's probably intended date as string, based on weekday and time (if mensa is open, today, if closed tommorows or mondays date!)
    
    beilagen = food[date]["sidedish"]
    
    if date == todays_date: #Wenn der heutige Tag noch relevant ist, kommt die heutige vital msg
        option_msg = render_template('beilagen', beilagen=beilagen)
    else: #wenn der tag abweichend ist, wird alternativ informiert, dass die mensa zu hat
        option_msg = render_template('alt_beilagen', beilagen=beilagen)

    return question(option_msg)



@ask.intent("WeekdayIntent", mapping={'mydate': 'Weekday'})
 

def weekday_request(mydate):
    #Dieser Intent wird immer aufgerufen, wenn ein bestimmter Wochentag angegeben / angefragt wurde (wird aber leider manchmal mit leerem slot erkannt)
    date = misc.probable_date() #wie immer datumsangaben, dieses malals zurückfall-Wert, falls dieser intent ohne erkanntes datum aufgerufen wird
    
    if mydate=='': #diese if passiert, wenn wir ohne slot ungewollt in diesen Intent gelangen
        mydate=date
    
    #readable date konvertiert das nun feststehnde datum zu einem "readable" string (zu montag/di/mi/do/fr als string)
    readable_day = misc.get_readable_date(mydate)

    weekend_bool = misc.is_weekend(str(mydate)) #returns true if the requested date is a weekend
    if weekend_bool == True:
        #print "und das ist ein wochenende"
        mydate = date #indem Fall fallen wir aus das probable default Datum zurück, damit in jedem Fall eine informative Auskunft gegeben wird
    
    try: #ab hier funktioniert der intent genau wie welc msg, beilagen und vital intent
        food = mensa.read_json(mensa.check_json())
        dict(food)
    except: #wenn die session kein food und date hat, hat man nich mit welcomegestartet und muss die info erst holen
        food = mensa.scrape_pipeline() #get's a food dict or loading error as string
        if type(food)==str:
            error_handling(food)

    maindish = food[str(mydate)]["maindish"]
    veggiedish = food[str(mydate)]["veggiedish"]

    weekday_reply=render_template('specdate', wochentag=readable_day, maindish=maindish, veggiedish=veggiedish)
    
    #this was an attempt at grounding, maybe we just spoke about vitalmenü, so i check if such a dialouge_sate exists
    #also we should save the date the user is currently requesting for future queries 
    try:
        grounded = session.attributes['dialogue_state'] #if it exists, we save the date that was talked about here
        grounded['talked_date'] = str(mydate)           #and give it back as session attribute
        session.attributes['dialogue_state'] = grounded
    except: #wenn es keinen gibt, erstellen wir es
        grounded = {}
        grounded['talked_date'] = str(mydate) #saves what was talked about before 
        session.attributes["dialogue_state"] = grounded
    #unfortunately, this isn't included in the other intents yet 
    
    return question(weekday_reply)




@ask.intent("VeggieIntent")

def myveggie(): #works just like vital and beilange, just with the veggiemenü and voicelines
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
    else: #wenn der tag abweichend ist, wird alternativ informiert, das die mensa zu hat
        option_msg = render_template('alt_veggie_msg', veggiedish=veggiedish)

    return question(option_msg)
   


@ask.intent("FinalIntent")  #our default good bye msg =) 

def end_msg():
    goodbye = render_template('quitmsg')
    return statement(goodbye)





if __name__ == '__main__':

    app.run(debug=True)
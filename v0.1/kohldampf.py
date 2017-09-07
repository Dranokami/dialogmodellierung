#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import datetime
import web_scraper.fake_scrape as mensa
#import web_scraper.mensa_scraper  as mensa
import misc.misc as misc 

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


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
        date = session.attributes['date']
    except KeyError: #wenn die session kein food und date hat, hat man nich mit welcomegestartet und muss die info erst holen
        food = mensa.scrape_pipeline() #get's a food dict or loading error
        if type(food) == str:
            error_handling(food)
    todays_date=str(datetime.datetime.now()).split()[0]
    date = misc.probable_date() #get's probably intended date as string, based on weekday and time (if mensa is open, today, if closed tommorows or mondays date!)
    
    vital = food[date]["vital"]
    
    if date == todays_date: #Wenn der heutige Tag noch relevant ist, kommt die heutige vital msg
        option_msg = render_template('vitalmsg', vital=vital)
    else: #wenn der tag abweichend ist, wird alternativ informiert, das die mensa zu hat
        option_msg = render_template('alt_vitalmsg', vital=vital)
    
    return question(option_msg)



@ask.intent("BeilagenIntent")

def beilageninfo():
    try: 
        food = session.attributes['food']
        date = session.attributes['date']
    except KeyError: #wenn die session kein food und date hat, hat man nich mit welcomegestartet und muss die info erst holen
        food = mensa.scrape_pipeline() #get's a food dict or loading error as string
        if type(food)==str:
            error_handling(food)
    
    todays_date=str(datetime.datetime.now()).split()[0]
    date = misc.probable_date() #get's probably intended date as string, based on weekday and time (if mensa is open, today, if closed tommorows or mondays date!)
    
    beilagen = food[date]["beilagen"]
    
    if date == todays_date: #Wenn der heutige Tag noch relevant ist, kommt die heutige vital msg
        option_msg = render_template('beilagen', beilagen=beilagen)
    else: #wenn der tag abweichend ist, wird alternativ informiert, das die mensa zu hat
        option_msg = render_template('alt_beilagen', beilagen=beilagen)
    
    return question(option_msg)



@ask.intent("WeekdayIntent", mapping={'mydate': 'Weekday'})
 
def weekday_request(mydate):
    #todo: samstag /sonntag möglich machen als slot und abfangen
    readable_day = misc.get_readable_date(mydate)
    try:
        food = session.attributes['food']
        date = session.attributes['date']
    except KeyError: #wenn die session kein food und date hat, hat man nich mit welcomegestartet und muss die info erst holen
        food = mensa.scrape_pipeline() #get's a food dict or loading error as string
        if type(food)==str:
            error_handling(food)

    date = misc.probable_date() #get's probably intended date as string, based on weekday and time (if mensa is open, today, if closed tommorows or mondays date!)
    
    maindish = food[str(mydate)]["maindish"]
    veggiedish = food[str(mydate)]["veggiedish"]

    weekday_reply=render_template('specdate', wochentag=readable_day, maindish=maindish, veggiedish=veggiedish)

    return question(weekday_reply)



@ask.intent("FinalIntent")

def end_msg():
    goodbye = render_template('quitmsg')
    return statement(goodbye)


def error_handling(error):
    error_msg = render_template(error)
    return statement(error_msg)



if __name__ == '__main__':

    app.run(debug=True)
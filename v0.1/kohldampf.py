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


#This py get's handles all intents, external information about food get imported from the scraper, intented days (based on opening times) from misc function

@ask.launch

def new_game():

    food = mensa.scrape_pipeline() #get's a food dict or loading error
    if food == "Seite konnte nicht aufgerufen werden":
        welcome_msg = render_template('error_01')
    elif food == "Die Struktur der Seite stimmt nicht":
        welcome_msg = render_template('error_02')
    else:
        date = misc.probable_date() #get's probably intended date as string, based on weekday and time (if mensa is open, today, if closed tommorows or mondays date!)

        maindish = food[date]["maindish"]
        veggiedish = food[date]["veggiedish"]
        
        todays_date=str(datetime.datetime.now()).split()[0]
        if date == todays_date: #Wenn der heutige Tag noch relevant ist, kommt die Standard welcome msg
            welcome_msg = render_template('welcome', maindish=maindish, veggiedish=veggiedish)
            #print "heutiges datum ist relevant und wird vorgelesen"
        else: #wenn der tag abweichend ist, wird alternativ informiert, das die mensa zu hat
            welcome_msg = render_template('alt_welcome', maindish=maindish, veggiedish=veggiedish)
            #print "abweichendes datum soll vorgelesen werden"
        

        if type(food)==dict:
            session.attributes['food'] = food #übergibt das food attribut und relevante datum der session 
            session.attributes['date'] = date
            #session.attributes['numbers'] = numbers[::-1]  # reverse   
    
    return question(welcome_msg)


@ask.intent("MenuIntent")

def menuoptions():
    option_msg = render_template('menu_options')
    #session.attributes['numbers'] = numbers[::-1]  # reverse
    return question(option_msg)


@ask.intent("DayIntent")

def dayoptions():
    option_msg = render_template('day_options')
    #session.attributes['numbers'] = numbers[::-1]  # reverse
    return question(option_msg)


@ask.intent("VitalIntent")

def vitalinfo():
    todays_date=str(datetime.datetime.now()).split()[0]
    food = session.attributes['food']
    date = session.attributes['date']
    vital = food[date]["vital"]

    if date == todays_date: #Wenn der heutige Tag noch relevant ist, kommt die heutige vital msg
        option_msg = render_template('vitalmsg', vital=vital)
    else: #wenn der tag abweichend ist, wird alternativ informiert, das die mensa zu hat
        option_msg = render_template('alt_vitalmsg', vital=vital)
    return question(option_msg)


@ask.intent("BeilagenIntent")

def beilageninfo():
    todays_date=str(datetime.datetime.now()).split()[0]
    food = session.attributes['food']
    date = session.attributes['date']
    beilagen = food[date]["beilagen"]

    if date == todays_date: #Wenn der heutige Tag noch relevant ist, kommt die heutige vital msg
        beilagen = session.attributes["food"]["date"]["beilagen"]
        option_msg = render_template('beilagen', beilagen=beilagen)
    else: #wenn der tag abweichend ist, wird alternativ informiert, das die mensa zu hat
        option_msg = render_template('alt_beilagen', beilagen=beilagen)
    return question(option_msg)


@ask.intent("FinalIntent")

def end_msg():
    goodbye = render_template('quitmsg')
    return statement(goodbye)



if __name__ == '__main__':

    app.run(debug=True)
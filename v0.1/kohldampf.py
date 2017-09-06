#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import datetime
from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch

def new_game():

    day_and_mensa = date_and_mensa_open()
    food = {
    "2017-09-05" : {"maindish":"Alaskaseelachsfilet", "veggiedish":u"gefüllte Paprikaschote"},
    "2017-09-06" : {"maindish":u"Hähnchenkeule", "veggiedish":u"Käsemedaillon"},
    "2017-09-07" : {"maindish":u"Cordon Bleu", "veggiedish":u"Frühlingsröllchen"}  
    }
    
    if day_and_mensa[1] == "heute":
        maindish = food[day_and_mensa[0]]["maindish"]
        veggiedish = food[day_and_mensa[0]]["veggiedish"]
        welcome_msg = render_template('welcome', maindish=maindish, veggiedish=veggiedish)
    else:
        tommorow = str(datetime.datetime.now() + datetime.timedelta(days=1)).split()[0]
        maindish = food[tommorow][0]["maindish"]
        veggiedish = food[tommorow][1]["veggiedish"]
        welcome_msg = render_template('alt_welcome', maindish=maindish, veggiedish=veggiedish)
    return question(welcome_msg)


@ask.intent("MenuIntent")

def menuoptions():
    option_msg = render_template('menu')

    #session.attributes['numbers'] = numbers[::-1]  # reverse
    return question(option_msg)

@ask.intent("DayIntent")

def dayoptions():
    option_msg = render_template('day')
    #session.attributes['numbers'] = numbers[::-1]  # reverse
    return question(option_msg)

@ask.intent("VitalIntent")

def vitalinfo():
    vital = "Lecker essen"
    option_msg = render_template('vitalmsg', vital = vital)

    #session.attributes['numbers'] = numbers[::-1]  # reverse
    return question(option_msg)


@ask.intent("BeilagenIntent")

def beilageninfo():
    sidedish = "Bulgur"
    option_msg = render_template('beilagen', sidedish=sidedish)

    #session.attributes['numbers'] = numbers[::-1]  # reverse
    return question(option_msg)


@ask.intent("FinalIntent")

def end_msg():
    goodbye = render_template('quitmsg')

    return statement(goodbye)


def date_and_mensa_open():
    #uses datetime and returns a list with [0]the concrete day/month for the db query and tommorow or today regarding a closed mensa 
    now_is=str(datetime.datetime.now()).split()
    #now now_is[0] looks like 2017-09-05 and [1] like 19:46:07.851512
    hour=int(now_is[1].split(":")[0])
    if hour <= 13:
        mensa="heute"
    elif hour >= 15:
        mensa="morgen"
    elif hour == 14:
        if int(now_is[1].split(":")[1]) >=30:
            mensa="morgen"
        else:
            mensa="heute"
    return [now_is[0], mensa]

if __name__ == '__main__':

    app.run(debug=True)
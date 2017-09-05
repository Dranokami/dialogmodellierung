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
    "2017-09-05" : ["Alaskaseelachsfilet",u"gefüllte Paprikaschote"],
    "2017-09-06" : [u"Hähnchenkeule", u"Käsemedaillon"],
    "2017-09-07" : [u"Cordon Bleu", u"Frühlingsröllchen"]
    #usw    
    }
    
    if day_and_mensa[1] == "heute":
        maindish = food[day_and_mensa[0]][0]
        veggiemeal = food[day_and_mensa[0]][1]
        welcome_msg = render_template('welcome', maindish=maindish, veggiemeal=veggiemeal)
    else:
        tommorow = str(datetime.datetime.now() + datetime.timedelta(days=1)).split()[0]
        maindish = food[tommorow][0]
        veggiemeal = food[tommorow][1]
        alt_welcome=welcome_msg = render_template('alt_welcome', maindish=maindish, veggiemeal=veggiemeal)

    return question(welcome_msg)


@ask.intent("YesIntent")

def next_round():

    
    round_msg = render_template('round', numbers=numbers)

    session.attributes['numbers'] = numbers[::-1]  # reverse
    return question(round_msg)


@ask.intent("AnswerIntent", convert={'first': int, 'second': int, 'third': int})

def answer(first, second, third):

    winning_numbers = session.attributes['numbers']

    if [first, second, third] == winning_numbers:

        msg = render_template('win')

    else:

        msg = render_template('lose')

    return statement(msg)


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
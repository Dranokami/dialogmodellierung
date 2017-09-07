#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

def scrape_pipeline():
    random_eve = random.randint(1,10)
    if random_eve==1:       
        food = "Seite konnte nicht aufgerufen werden"
    elif random_eve==2:
        food = "Die Struktur der Seite stimmt nicht"
    else:
        food = {"2017-09-07":{"maindish":"Alaska", "veggiedish":"Tofu", "vital":"huhn","beilagen":"kartoffel"},
                "2017-09-08":{"maindish":u"hähnchenschnitzel", "veggiedish": u"frühlingsröllchen","vital": u"döner","beilagen":"bulgur"}
                }

    return food

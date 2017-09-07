#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup
import urllib
import re
import datetime


def scrape_pipeline():
    URL = "http://www.studierendenwerk-bielefeld.de/essen-trinken/essen-und-trinken-in-mensen/bielefeld/mensa-gebaeude-x.html"
    mensa_doc = urllib.urlopen(URL).read()
    soup = BeautifulSoup(mensa_doc, 'html.parser')
    compiler = re.compile(r"[0-3][0-9]\.[0-1][0-9]\.20[0-9][0-9]")
    datum_liste = list()

    for f in soup.findAll('h2'):
        found = compiler.search(f.text)
        if found:
            datum_liste.append(datetime.datetime.strptime(found.group(),"%d.%m.%Y").strftime("%Y-%m-%d"))
    for tag in soup.findAll('sup'):
        tag.decompose()
    dishes_dict = dict()
    dish_list = []
    for heading in soup.findAll('div'):
    if heading.get('class') == [u'mensa', u'plan']:
        
        raw_path = heading.div.table.tbody.tr
        #Tagesmenpü
        #print raw_path.td.h3.strong.text, ": ", raw_path.td.p.p.text # 
        temp_dict_main = dict()
        temp_dict_main['maindish'] =  raw_path.td.p.p.text
        #Vegetarisch
        #print raw_path.next_sibling.next_sibling.td.h3.strong.text, ": ", raw_path.next_sibling.next_sibling.td.p.p.text 
        temp_dict_veggie = dict()
        temp_dict_veggie['veggiedish'] =  raw_path.next_sibling.next_sibling.td.p.p.text
        #Mensa Vital
        #print raw_path.next_sibling.next_sibling.next_sibling.next_sibling.td.h3.strong.text, ": ", raw_path.next_sibling.next_sibling.next_sibling.next_sibling.td.p.p.text
        temp_dict_vital = dict()
        temp_dict_vital['vital'] = raw_path.next_sibling.next_sibling.next_sibling.next_sibling.td.p.p.text
        
        #print raw_path.next_sibling.next_sibling.td.p.p.next_sibling.next_sibling.text #beilagen
        #print raw_path.td.p.p.next_sibling.next_sibling.text   #Beilagen
        temp_dict_beilage = dict()
        temp_dict_beilage['sidedish'] = raw_path.td.p.p.next_sibling.next_sibling.text
        
        dish_list.append(temp_dict_main)
        dish_list.append(temp_dict_veggie)
        dish_list.append(temp_dict_beilage)
        dish_list.append(temp_dict_vital)
            
        #print "------------------------------------------------------------------------------------"


    return dict(zip(datum_liste,dish_list))
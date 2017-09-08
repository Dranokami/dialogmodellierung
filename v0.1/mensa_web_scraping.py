# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import datetime
import json
import re
import os.path


def check_json():
    ''' function checks if actual json is available
    returns true | false'''
    # TODO: überprüfen, ob os.path() in Linux auf gleiche Weise funktioniert, wie in Win 
    # der pfad muss an jeweiligen "Start-ort" angepasst werden (also von wo das Modul geladen und gestartet wird)
    # ich weiß nicht, ob es (für unsere Zwecke) ausreichen würde einfach ein "./web_scraper/" oder so davor zu setzen
    # glaube zudem, dass zwischen Windoof- und Unix-Systemen einen unterschied macht, ob man "/" oder "\"
    # vielleicht gibt die doku ja was her?
    
    today = datetime.date.today()
    last_monday = today + datetime.timedelta(days=-today.weekday(), weeks=0)
    if os.path.isfile(str(last_monday)[:10] + ".json"):
        f = os.path.basename(str(last_monday)[:10] + ".json")
        return f
    else:
        return False
        
def read_json(file_name):
    ''' function reads json from folder
    returns json'''
    with open(file_name, 'r') as jfile:
        j_file = json.load(jfile)
    return j_file

def download_page(URL="http://www.studierendenwerk-bielefeld.de/essen-trinken/essen-und-trinken-in-mensen/bielefeld/mensa-gebaeude-x.html"):
    ''' function downloads the information of the current week
    returns text | error message'''
    r = requests.get(URL)
    if r.status_code == 200:
        r.encoding = "utf-8"
        return r.text
    else:
        return "Seite existiert nicht" #Wie soll scraper_pipeline darauf zugreifen?


def parse_web_page(doc):
    '''parses mensa structure
    returns food information as dict'''
    datumsliste = list()
    dishes_day_by_day = list()
    
    # parsing via beautifulsoup
    soup = BeautifulSoup(doc, 'html.parser')

    # sind in der ersten Woche 5 Menüs?
    # sind in der ersten und zweiten woche 10 menüs?
    
    #nächste Woche aufrufen
    for link in soup.find_all('a'):
        if link.get('title') == u"» nächste Woche":
            next_week_link = "http://www.studierendenwerk-bielefeld.de"+link['href']
            next_week_page = download_page(URL=next_week_link)
            if next_week_page:
                combined_doc = doc + next_week_page 

    soup = BeautifulSoup(combined_doc, 'html.parser')
    for tag in soup.findAll('sup'):
        tag.decompose()

    # find datetime to sort dishes per date
    compiler = re.compile(r"[0-3][0-9]\.[0-1][0-9]\.20[0-9][0-9]")
    datumsliste = [datetime.datetime.strptime(compiler.search(f.text).group(),"%d.%m.%Y").strftime("%Y-%m-%d") for f in soup.findAll('h2') if compiler.search(f.text)]

    # .strftime("%Y-%m-%d") if we want to change the date structure we have to append on (...)-.
    # exctract dishes

    for heading in soup.findAll('div', class_='mensa plan'):
        if not heading:
            print "error_01"
             # testing ob struktur übereinstimmt --> none-type?
        else:
            temp_dict = dict()
            raw_path = heading.div.table.tbody.tr
            temp_dict['maindish'] = raw_path.td.p.p.text
            temp_dict['veggiedish'] = raw_path.next_sibling.next_sibling.td.p.p.text
            temp_dict['vital'] = raw_path.next_sibling.next_sibling.next_sibling.next_sibling.td.p.p.text
            #raw_path.next_sibling.next_sibling.td.p.p.next_sibling.next_sibling.text
            sidedishes_set = set(raw_path.next_sibling.next_sibling.td.p.p.next_sibling.next_sibling.text.split(',')).union(set(raw_path.td.p.p.next_sibling.next_sibling.text.split(',')))

            temp_dict['sidedish'] = u', '.join(sidedishes_set)
            dishes_day_by_day.append(temp_dict)
    return dict(zip(datumsliste, dishes_day_by_day))

def convert_json(food_dict):
    '''function takes the food info and converts that to a json file
    returns json file | error message '''
    if type(food_dict) == dict:  # das kann dann später weg. nur noch diese json.dump(dictionary)
        return json.dumps(food_dict)
    else:
        print "error_02"


def save2json(food_dict):
    ''' saves the json_file in folder'''
    today = datetime.date.today()
    week_date = today + datetime.timedelta(days=-today.weekday(), weeks=0)
    with open(str(week_date) + '.json', 'w') as outputfile:
        return json.dump(food_dict,outputfile)


def scrape_pipeline():
    ''' mother function that merges all functions together
    returns dict for alexa '''
    # Kommentar von Julia: ich schätze, dass es an dieser Stelle zu einem Fehler kann, \
    #weil eine Text-Datei weitergereicht wurde (wenn überhaupt mal eine .json generiert wurde) \
    # denn sobald hier die Datei eingelesen wird, enststeht ein STRING und der löst in der kohldampf.py an vielen Stellen einen ERROR aus
    
    #checked_json = check_json()
    #if checked_json:
    #    print 'hello'
    #    return read_json(checked_json)
    #else:
    if True:
        page_content = download_page()
        if page_content:
            food_dict = parse_web_page(page_content)
            json_file = convert_json(food_dict)
            if json_file:
                save2json(json_file)
                return food_dict
            else:
                print "error_01"
        else:
            print "error_02"

if __name__ == '__main__':
	scrape_pipeline()
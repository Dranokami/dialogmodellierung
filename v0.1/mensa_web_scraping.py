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
    
    today = datetime.date.today() #asking for the current date 
    last_monday = today + datetime.timedelta(days=-today.weekday(), weeks=0) # asking for the date of the last monday
    if os.path.isfile(str(last_monday)[:10] + ".json"): #when .json already exists, returning json with food information
        return os.path.basename(str(last_monday)[:10] + ".json")
    else:
        return False
        
def read_json(file_name):
    ''' function reads json from folder
    returns json content'''
    with open(file_name, 'r') as jfile:
        json_content = json.load(jfile)
    return json_content

def download_page(URL="http://www.studierendenwerk-bielefeld.de/essen-trinken/essen-und-trinken-in-mensen/bielefeld/mensa-gebaeude-x.html"): #url can be replaced
    ''' function downloads the information of the current week 
    returns website content in xml structure'''
    r = requests.get(URL)
    if r.status_code == 200:
        r.encoding = "utf-8"
        return r.text


def parse_web_page(doc):
    '''parses mensa structure
    returns food information as dict'''
    datumsliste = list()
    dishes_day_by_day = list()
    
    # parsing via beautifulsoup
    soup = BeautifulSoup(doc, 'html.parser')

    # here we should have implemented a structure checking. 
    # first part should contain five keys in the food_dict
    
    # parsing next weeks mensa info
    for link in soup.find_all('a'):
        if link.get('title') == u"» nächste Woche":
            next_week_link = "http://www.studierendenwerk-bielefeld.de"+link['href']
            next_week_page = download_page(URL=next_week_link)
            if next_week_page:
                combined_doc = doc + next_week_page 

    soup = BeautifulSoup(combined_doc, 'html.parser')
    for tag in soup.findAll('sup'):
        tag.decompose()
        
    # checking if dictionary contains ten keys. If not, error message
    
    # finding datetime to sort dishes per date
    compiler = re.compile(r"[0-3][0-9]\.[0-1][0-9]\.20[0-9][0-9]")
    datumsliste = [datetime.datetime.strptime(compiler.search(f.text).group(),"%d.%m.%Y").strftime("%Y-%m-%d") for f in soup.findAll('h2') if compiler.search(f.text)]

    # .strftime("%Y-%m-%d") if we want to change the date structure we have to append on (...)-.
    
    # exctracting dishes
    for heading in soup.findAll('div', class_='mensa plan'):
        if not heading:
            print "error_01"# testing --> none-type?
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
    return dict(zip(datumsliste, dishes_day_by_day)) #provides the mensa plan with date as key and dishes per date as values; these dishes are keys in an inner dictionary that has the extracted dishes as values

def convert_json(food_dict):
    '''function takes the food info and converts that to a json file
    returns json file'''
    if type(food_dict) == dict:  
        return json.dumps(food_dict) # creating a json that contains the food dict
        
def save2json(food_dict):
    ''' saves the json_file in folder'''
    today = datetime.date.today()
    week_date = today + datetime.timedelta(days=-today.weekday(), weeks=0)
    with open(str(week_date) + '.json', 'w') as outputfile:
        return json.dump(food_dict,outputfile)


def scrape_pipeline():
    ''' function that merges all functions together
    returns dict for alexa '''
    
    ## meta information: the first part gives occationally an error. Therefore, we commented that out.
    #checked_json = check_json()
    #if checked_json:
    #    print 'hello'
    #    return read_json(checked_json)
    #else:
    if True: # the second part calls the functions from above: the page is called up, parsed and the infomation is extraced and transmitted to a dictionary. 
    page_content = download_page()
    if page_content:
        food_dict = parse_web_page(page_content)
        json_file = convert_json(food_dict)
        if json_file:
            save2json(json_file)
            return food_dict # dictionary is transmitted to the alexa connection.
        else:
            print "error_01"
    else:
        print "error_02"

if __name__ == '__main__':
	scrape_pipeline()

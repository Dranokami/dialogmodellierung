
# coding: utf-8

# In[1]:

from bs4 import BeautifulSoup
import requests
import datetime
import os.path


# In[14]:

def check_json():
    today = datetime.date.today()
    last_monday = today + datetime.timedelta(days=-today.weekday(), weeks=0)
    return os.path.isfile(str(last_monday)[:10]+".json")


# In[15]:

check_json()


# In[16]:

def download_page(page_existing=False):
    URL = "http://www.studierendenwerk-bielefeld.de/essen-trinken/essen-und-trinken-in-mensen/bielefeld/mensa-gebaeude-x.html"
    r = requests.get(URL)
    if r.status_code == 200:
        r.encoding = "utf-8"
        return r.text
    else:
        return "funzt nicht" #Wie soll scraper_pipeline darauf zugreifen?


# In[18]:

download_page()


# In[3]:

URL = "http://www.studierendenwerk-bielefeld.de/essen-trinken/essen-und-trinken-in-mensen/bielefeld/mensa-gebaeude-x.html"
mensa_doc = urllib.urlopen(URL).read()
soup = BeautifulSoup(mensa_doc, 'html.parser')


# In[4]:

#eliminate <sup>-tags
for tag in soup.findAll('sup'):
    tag.decompose()


# In[8]:

#extract dates
# fehlerabfrage
compiler = re.compile(r"[0-3][0-9]\.[0-1][0-9]\.20[0-9][0-9]")
datumliste = [datetime.datetime.strptime(compiler.search(f.text).group(),"%d.%m.%Y").strftime("%Y-%m-%d") for f in soup.findAll('h2') if compiler.search(f.text)]


# In[6]:

#exctract dishes
for heading in soup.findAll('div'):
    temp_dict = dict()
    if heading.get('class') == [u'mensa', u'plan']:
        raw_path = heading.div.table.tbody.tr
        temp_dict['maindish'] =  raw_path.td.p.p.text 
        temp_dict['veggiedish'] =  raw_path.next_sibling.next_sibling.td.p.p.text
            
        temp_dict['vital'] = raw_path.next_sibling.next_sibling.next_sibling.next_sibling.td.p.p.text
            
        raw_path.next_sibling.next_sibling.td.p.p.next_sibling.next_sibling.text
        sidedishes_set = set(raw_path.next_sibling.next_sibling.td.p.p.next_sibling.next_sibling.text.split(',')).union(set(raw_path.td.p.p.next_sibling.next_sibling.text.split(',')))
        temp_dict['sidedish'] = ', '.join(sidedishes_set)
        dishes_day_by_day.append(temp_dict)


# In[20]:

def parse_web_page(doc):
    '''parses mensa structure'''
    datumsliste = list()
    dishes_day_by_day = list()
   
    # parsing via beautifulsoup
    soup = BeautifulSoup(doc, 'html.parser')
    for tag in soup.findAll('sup'):
        tag.decompose()
    # find datetime to sort dishes per date
    compiler = re.compile(r"[0-3][0-9]\.[0-1][0-9]\.20[0-9][0-9]")
    datumsliste = [datetime.datetime.strptime(compiler.search(f.text).group(),"%d.%m.%Y").strftime("%Y-%m-%d") for f in soup.findAll('h2') if compiler.search(f.text)]
    # .strftime("%Y-%m-%d") if we want to change the date structure we have to append on (...)-.

    # exctract dishes
    for heading in soup.findAll('div'):
        # testing ob struktur übereinstimmt --> none-type?
        temp_dict = dict()
        if heading.get('class') == [u'mensa', u'plan']:
            raw_path = heading.div.table.tbody.tr
            temp_dict['maindish'] = raw_path.td.p.p.text
            temp_dict['veggiedish'] = raw_path.next_sibling.next_sibling.td.p.p.text
            temp_dict['vital'] = raw_path.next_sibling.next_sibling.next_sibling.next_sibling.td.p.p.text

            raw_path.next_sibling.next_sibling.td.p.p.next_sibling.next_sibling.text
            sidedishes_set = set(
                raw_path.next_sibling.next_sibling.td.p.p.next_sibling.next_sibling.text.split(',')).union(
                set(raw_path.td.p.p.next_sibling.next_sibling.text.split(',')))
            temp_dict['sidedish'] = ', '.join(sidedishes_set)
            dishes_day_by_day.append(temp_dict)

    food_dict = dict(zip(datumsliste, dishes_day_by_day))

    if type(return_) == dict:
        return json.dumps(food_dict)
    else:
        return "Die Struktur der Seite stimmt nicht"
   
        #, sort_keys = True, indent = 4)
       # json has following structure: {'KW': {date1: {dish1: 'xxx'},
                                               # dish2: 'xxx'}...,
                                           #date1: {...}}


# In[ ]:

def save_json(json_file):
    ''' saves the json_file in folder'''
    today = datetime.date.today()
    week_date = today+datetime.timedelta(days=-today.weekday(), weeks=0)

    with codecs.open(str(week_date)+'.json', 'w')as outputfile:
        outputfile.write(json_file)
       
        


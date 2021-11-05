import re
from urllib.request import Request, urlopen

import requests
from bs4 import BeautifulSoup
import pandas as pd

def load_all_post(page):
    item = page.find('ul', {'class' : 'pager'})
    last = item.find('a',{'title' : 'Go to last page'})
    link = str(last['href'])
    link = link.split('=')
    print(int(link[len(link)-1])-1)



HEADER = {'User-Agent': 'Mozilla/5.0'}
get_request = Request("https://www.nationaleatingdisorders.org/forums/covid-19",headers=HEADER)
page = urlopen(get_request).read()
get_page = BeautifulSoup(page,'lxml')

load_all_post(get_page)
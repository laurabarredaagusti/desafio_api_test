

from bs4 import BeautifulSoup as bs
import requests
import html
import json
from datetime import date

from variables import *

class KWh:
    path = kwh_price_path
    url = 'https://tarifaluzhora.es/'

    def __init__(self):
        pass
        self.create_soup()
        self.get_price()
        self.current_datetime()
        self.open_json()
        self.update_json()
    
    def create_soup(self):
        response = requests.get(self.url)
        html = response.content
        self.soup = bs(html, "lxml")
    
    def get_price(self):
        self.price = self.soup.find('span', class_='main_text').text[:-2]
        self.price = float(self.price)

    def current_datetime(self):
        today = date.today()
        self.current_date = today.strftime("%d/%m/%Y %H:%M:%S")

    def open_json(self):
        with open(self.path, 'r') as j:
            self.contents = json.loads(j.read())
    
    def update_json(self):
        
        self.contents[self.current_date] = self.price

        with open(self.path, 'w') as outfile:
            json.dump(self.contents, outfile)
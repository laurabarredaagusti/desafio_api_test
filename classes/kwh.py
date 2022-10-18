from bs4 import BeautifulSoup as bs
import requests
from datetime import date
from functions import *
from queries.queries import *

from variables import host, port, user, password, database

class GetKWh:
    host = host
    port = port
    user = user
    password = password
    database = database 
    price_kwh_date = price_kwh_date
    insert_date_price_kwh = insert_date_price_kwh

    url = 'https://tarifaluzhora.es/'

    def __init__(self):
        self.current_datetime()
        self.cursor = connect_database()
        self.exec_query()
        self.scrap()
        self.store_data()

    def current_datetime(self):
        today = date.today()
        self.current_date = today.strftime("%d/%m/%Y")

    def exec_query(self):
        self.price_kwh_date_var = [str(self.current_date)]
        self.records = exec_query_records(self.price_kwh_date, self.price_kwh_date_var, self.cursor)
    
    def scrap(self):
        if len(self.records) == 0:
            self.create_soup()
            self.get_price()
        else:
            self.price = self.records[0][0]
    
    def create_soup(self):
        response = requests.get(self.url)
        html = response.content
        self.soup = bs(html, "lxml")
    
    def get_price(self):
        self.price = self.soup.find('span', class_='main_text').text[:-2]

    def store_data(self):
        self.insert_date_price_kwh_var = (self.current_date, self.price)
        exec_query_no_records(self.insert_date_price_kwh, self.insert_date_price_kwh_var, self.cursor)
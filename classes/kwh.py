
import psycopg2
from bs4 import BeautifulSoup as bs
import requests
import html
import json
from datetime import date

from variables import host, port, user, password, database, kwh_price_path

class GetKWh:
    host = host
    port = port
    user = user
    password = password
    database = database 
    path = kwh_price_path

    url = 'https://tarifaluzhora.es/'

    def __init__(self):
        self.current_datetime()
        self.connect_database()
        self.exec_query()
        self.scrap()
        self.store_data()

    def current_datetime(self):
        today = date.today()
        self.current_date = today.strftime("%d/%m/%Y")

    def connect_database(self):
        self.db = psycopg2.connect(host=self.host,
                            port=self.port,
                            user=self.user,
                            password=self.password,
                            database=self.database)
        self.db.autocommit=True
        self.cursor = self.db.cursor()

    def exec_query(self):
        query = '''SELECT "Price" FROM price_kwh WHERE "Date" = \'''' + str(self.current_date) + '''\';'''
        self.cursor.execute(query)
        self.records = self.cursor.fetchall()
    
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
        query = '''INSERT INTO price_kwh ("Date", "Price") VALUES (\'''' + self.current_date + '''\', \'''' + self.price + '''\');'''
        self.cursor.execute(query)
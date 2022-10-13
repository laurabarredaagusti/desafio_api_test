from flask import jsonify
import psycopg2

from variables import *

class Category:
    host = host
    port = port
    user = user
    password = password
    database = database 

    def __init__(self, category):
        self.category = category

        self.connect_database()
        self.create_cursor()
        self.exec_query()
        self.get_dict()
        self.get_json()

    def connect_database(self):
        self.db = psycopg2.connect(host=self.host,
                            port=self.port,
                            user=self.user,
                            password=self.password,
                            database=self.database)
        self.db.autocommit=True

    def create_cursor(self):
        self.cursor = self.db.cursor()

    def exec_query(self):
        query = 'SELECT "Brand", "Model" FROM ' + self.category
        self.cursor.execute(query)
        self.records = self.cursor.fetchall()

    def get_dict(self):
        list_brand = [elem[0] for elem in self.records]
        list_model = [elem[1] for elem in self.records]

        self.dict = {'Brand': list_brand,
                     'Model' : list_model}

    def get_json(self):
        self.json = jsonify(self.dict)
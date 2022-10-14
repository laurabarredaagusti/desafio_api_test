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
        self.get_brand_list()
        self.get_equivalences()
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

    def get_brand_list(self):
        self.brand_list = [elem[0] for elem in self.records]
        self.brand_list = list(set(self.brand_list))
        self.brand_list = [elem[1:-1] for elem in self.brand_list]

    def get_equivalences(self):
        self.model_list = [elem[1] for elem in self.records]
        self.model_list = list(set(self.model_list))
        self.model_list = [elem[1:-1] for elem in self.model_list]
        self.equiv_dict = {'Brand': self.brand_list,
                           'Model' : self.model_list}

    def get_json(self):
        self.equiv_dict = {'Brand': self.brand_list,
                           'Model_by_brand' : self.equiv_dict}

        self.json = jsonify(self.equiv_dict)
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
        self.brand_list_mod = [elem[1:-1].lower() for elem in self.brand_list]

    def get_equivalences(self):
        self.equiv_dict = dict((key, []) for key in self.brand_list)
        for elem in self.records:
            brand = elem[0]
            model = elem[1]
            self.equiv_dict[brand].append(model[1:-1].lower())
            self.equiv_dict_new = dict(zip(self.brand_list_mod, list(self.equiv_dict.values())))

    def get_json(self):
        self.equiv_dic_totalt = {'Brand': self.brand_list_mod,
                           'Model_by_brand' : self.equiv_dict_new}

        self.json = jsonify(self.equiv_dic_totalt)
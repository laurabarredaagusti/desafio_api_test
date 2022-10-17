from flask import jsonify
import psycopg2
import json

from variables import host, port, user, password, database

class Category:
    host = host
    port = port
    user = user
    password = password
    database = database 

    def __init__(self, category, session_id):
        self.product_category = category
        self.session_id = session_id

        self.connect_database()
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
        self.cursor = self.db.cursor()

    def exec_query(self):
        query = '''SELECT "Brand", "Model" FROM products WHERE "Product_family" = \'''' + self.product_category + '''\';'''
        self.cursor.execute(query)
        self.records = self.cursor.fetchall()

    def get_brand_list(self):
        self.brand_list = [elem[0] for elem in self.records]
        self.brand_list = list(set(self.brand_list))

    def get_equivalences(self):
        self.equiv_dict = dict((key, []) for key in self.brand_list)
        for elem in self.records:
            brand = elem[0]
            model = elem[1]
            self.equiv_dict[brand].append(model)
            self.equiv_dict_new = dict(zip(self.brand_list, list(self.equiv_dict.values())))

    def get_json(self):
        self.equiv_dic_total = {'Session_id': self.session_id,
                                'Brand': self.brand_list,
                                'Model_by_brand' : self.equiv_dict_new}

        self.json = jsonify(self.equiv_dic_total)
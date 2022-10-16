from flask import jsonify
import json
import psycopg2
from variables import *

class Calculate:
    host = host
    port = port
    user = user
    password = password
    database = database 
    store_data_path = store_data_path
    def __init__(self, session_id, arguments_list):

        self.arguments_list = arguments_list
        
        self.session_id = session_id
        self.brand = arguments_list[0]
        self.model = arguments_list[1]
        self.hours_day = float(arguments_list[2])
        self.price_kwh = float(arguments_list[3])
        self.current_datetime = arguments_list[4]
        
        self.connect_database()
        self.create_cursor()
        self.exec_query()
        self.cal_cycles()
        self.get_dict()
        self.get_json()
        self.read_data_json()
        self.store_data_dict()
        self.update_json()

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
        query = '''SELECT "Consumption", "Product_family" FROM products WHERE "Brand" = \'''' + self.brand + '''\' AND "Model" = \'''' + self.model + '''\';'''
        self.cursor.execute(query)
        self.records = self.cursor.fetchall()
        self.consumption = float(self.records[0][0])
        self.product_family = self.records[0][1]

    def cal_cycles(self):
        n_weeks_month = 365 / 12 / 7
        self.cost = self.consumption * self.price_kwh *  self.hours_day  * n_weeks_month

    def cal_kwh(self, n_hours=24):
        n_days_month = 365 / 12 
        self.cost = self.consumption * self.price_kwh * n_hours * n_days_month
        print(self.cost)

    def get_dict(self):
        self.dict = {'Cost': str(self.cost)}

    def get_json(self):
        self.json = jsonify(self.dict)

    def read_data_json(self):
        with open(self.store_data_path, 'r') as j:
            self.contents = json.loads(j.read())

    def store_data_dict(self):
        self.arguments_list.append(self.cost)
        self.arguments_list.append(self.product_family)
        self.data_dict = {}
        for index, data in enumerate(store_data):
            self.data_dict[data] = self.arguments_list[index]

    def update_json(self):
        self.contents[self.session_id] = self.data_dict
        with open(self.store_data_path, 'w') as outfile:
            json.dump(self.contents, outfile)


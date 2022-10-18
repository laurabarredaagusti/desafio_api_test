from flask import jsonify
import json
import psycopg2
from variables import host, port, user, password, database

class Calculate:
    host = host
    port = port
    user = user
    password = password
    database = database 

    def __init__(self, session_id, arguments_list):

        self.arguments_list = arguments_list
        
        self.session_id = session_id
        self.brand = arguments_list[0]
        self.model = arguments_list[1]
        self.time = float(arguments_list[2])
        self.price_kwh = float(arguments_list[3])
        self.current_datetime = arguments_list[4]
        
        self.connect_database()
        self.get_brand_model()
        self.get_consumption_family()
        self.get_type_consumption()
        self.decide_calculator()
        self.store_data()
        self.return_json()

    def connect_database(self):
        self.db = psycopg2.connect(host=self.host,
                            port=self.port,
                            user=self.user,
                            password=self.password,
                            database=self.database)
        self.db.autocommit=True
        self.cursor = self.db.cursor()

    def exec_query(self, query):
        self.cursor.execute(query)
        self.records = self.cursor.fetchall()

    def get_brand_model(self):
        if self.brand == 0 and self.model == 0:
            query = '''SELECT "Brand", "Model" FROM user_search WHERE "Session_id" = \'''' + self.session_id + '''\';'''
            self.exec_query(query)
            self.brand = self.records[0][0]
            self.model = self.records[0][1]

    def get_consumption_family(self):
        query = '''SELECT "Consumption", "Product_family" FROM products WHERE "Brand" = \'''' + self.brand + '''\' AND "Model" = \'''' + self.model + '''\';'''
        self.exec_query(query)
        print(self.brand)
        print(self.model)
        self.consumption = float(self.records[0][0])
        self.product_family = self.records[0][1]

    def get_type_consumption(self):
        query = '''SELECT "Consumption_type" FROM product_family WHERE "Product_family" = \'''' + self.product_family + '''\';'''
        self.exec_query(query)
        self.consumption_type = self.records[0][0]

    def decide_calculator(self):
        if self.consumption_type == 'hour':
            self.cal_kwh()
        else:
            self.cal_cycles()

    def cal_cycles(self):
        n_weeks_month = 365 / 12 / 7
        self.cost = self.consumption * self.price_kwh *  self.time  * n_weeks_month

    def cal_kwh(self, n_hours=24):
        n_days_month = 365 / 12 
        self.cost = self.consumption * self.price_kwh * self.time * n_days_month 

    def store_data(self):        
        query = '''UPDATE user_search 
        SET 
            "Brand" = \'''' + self.brand + '''\', 
            "Model" = \'''' + self.model + '''\', 
            "Hours_day" = \'''' + str(self.time) + '''\', 
            "Price_kwh" = \'''' + str(self.price_kwh) + '''\', 
            "Datetime" = \'''' + str(self.current_datetime) + '''\', 
            "Cost" = \'''' + str(self.cost) + '''\', 
            "Product_family" = \'''' + self.product_family + '''\' 
        WHERE
            "Session_id" = \'''' + str(self.session_id) + '''\';'''
            
        
        self.cursor.execute(query)

    def return_json(self):
        self.json = {'Cost': str(round(self.cost, 2))}
        self.json = jsonify(self.json)





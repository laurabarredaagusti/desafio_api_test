from flask import jsonify
from functions import *

class Calculate:

    def __init__(self, session_id, arguments_list):

        self.arguments_list = arguments_list
        
        self.session_id = session_id
        self.brand1 = arguments_list[0]
        self.model1 = arguments_list[1]
        self.brand2 = arguments_list[2]
        self.model2 = arguments_list[3]
        self.time = float(arguments_list[4])
        self.price_kwh = float(arguments_list[5])
        self.current_datetime = arguments_list[6]
        
        self.cursor = connect_database()
        self.get_brand_model()
        self.get_consumption_family()
        self.get_type_consumption()
        self.decide_calculator()
        self.store_data()
        self.return_json()

    def get_brand_model(self):
        if self.brand1 == 0 and self.model1 == 0 and self.brand2 == 0 and self.model2 == 0:
            query = '''SELECT "Brand1", "Model1", "Brand2", "Model2" 
                       FROM user_search 
                       WHERE "Session_id" = \'''' + self.session_id + '''\';'''
            self.records = exec_query_records(query, self.cursor)
            self.brand1 = self.records[0][0]
            self.model1 = self.records[0][1]
            self.brand2 = self.records[0][2]
            self.model2 = self.records[0][3]

    def get_consumption_family(self):
        query = '''SELECT "Consumption", "Product_family" FROM products 
                   WHERE ("Brand" = \'''' + self.brand1 + '''\' AND "Model" = \'''' + self.model1 + '''\')
                   OR ("Brand" = \'''' + self.brand2 + '''\' AND "Model" = \'''' + self.model2 + '''\');'''
        self.records = exec_query_records(query, self.cursor)
        self.consumption1 = float(self.records[0][0])
        self.product_family = self.records[0][1]
        self.consumption2 = float(self.records[1][0])

    def get_type_consumption(self):
        query = '''SELECT "Consumption_type" 
                   FROM product_family 
                   WHERE "Product_family" = \'''' + self.product_family + '''\';'''
        self.records = exec_query_records(query, self.cursor)
        self.consumption_type = self.records[0][0]

    def cal_cycles(self, consumption, time):
        n_weeks_month = 365 / 12 / 7
        return consumption * self.price_kwh *  time  * n_weeks_month

    def cal_kwh(self, consumption, time=24):
        n_days_month = 365 / 12 
        return consumption * self.price_kwh * time * n_days_month 

    def decide_calculator(self):
        if self.consumption_type == 'hour' or self.consumption_type == 'permanent':
            self.cost_1 = self.cal_kwh(self.consumption1, self.time)
            self.cost_2 = self.cal_kwh(self.consumption2, self.time)
        else:
            self.cost_1 = self.cal_cycles(self.consumption1, self.time)
            self.cost_2 = self.cal_cycles(self.consumption2, self.time)

    def store_data(self):        
        query = '''UPDATE user_search 
        SET 
            "Brand1" = \'''' + self.brand1 + '''\', 
            "Model1" = \'''' + self.model1 + '''\', 
            "Brand2" = \'''' + self.brand2 + '''\', 
            "Model2" = \'''' + self.model2 + '''\', 
            "Hours_day" = \'''' + str(self.time) + '''\', 
            "Price_kwh" = \'''' + str(self.price_kwh) + '''\', 
            "Datetime" = \'''' + str(self.current_datetime) + '''\', 
            "Cost1" = \'''' + str(self.cost_1) + '''\', 
            "Cost2" = \'''' + str(self.cost_2) + '''\', 
            "Product_family" = \'''' + self.product_family + '''\' 
        WHERE
            "Session_id" = \'''' + str(self.session_id) + '''\';'''
        exec_query_no_records(query, self.cursor)

    def store_data(self):    
        self.time = str(self.time)
        self.price_kwh = str(self.price_kwh) 
        self.current_datetime = str(self.current_datetime)    
        query = f'''UPDATE user_search 
        SET 
            "Brand1" = \'{self.brand1}\', 
            "Model1" = \'{self.model1}\', 
            "Brand2" = \'{self.brand2}\', 
            "Model2" = \'{self.model2}\', 
            "Hours_day" = \'{self.time}\', 
            "Price_kwh" = \'{self.price_kwh}\', 
            "Datetime" = \'{self.current_datetime}\', 
            "Cost1" = \'''' + str(self.cost_1) + '''\', 
            "Cost2" = \'''' + str(self.cost_2) + '''\', 
            "Product_family" = \'''' + self.product_family + '''\' 
        WHERE
            "Session_id" = \'''' + str(self.session_id) + '''\';'''
        exec_query_no_records(query, self.cursor)

    f'A function without return statement returns {saludo}'

    def return_json(self):
        self.json = {'Cost1': str(round(self.cost_1, 2)),
                     'Cost2': str(round(self.cost_2, 2))}
        self.json = jsonify(self.json)





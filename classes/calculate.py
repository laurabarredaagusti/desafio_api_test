from flask import jsonify
from functions import *
from queries.queries import *
from variables import *


class Calculate:

    cons_prod_fam_products = cons_prod_fam_products
    brands_models_usersearch = brands_models_usersearch
    consum_type_prodfamily = consum_type_prodfamily
    update_calculate = update_calculate
    labelDict = labelDict

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
        self.return_json()
        self.store_data()


    def get_brand_model(self):
        if self.brand1 == 0 and self.model1 == 0 and self.brand2 == 0 and self.model2 == 0:
            self.brands_models_usersearch_var = [self.session_id]
            self.records = exec_query_records(self.brands_models_usersearch, self.brands_models_usersearch_var, self.cursor)
            self.brand1 = self.records[0][0]
            self.model1 = self.records[0][1]
            self.brand2 = self.records[0][2]
            self.model2 = self.records[0][3]


    def get_consumption_family(self):
        self.cons_prod_fam_products_var = [self.brand1, self.model1, self.brand2, self.model2]
        self.records = exec_query_records(self.cons_prod_fam_products, self.cons_prod_fam_products_var, self.cursor)
        self.consumption1 = float(self.records[0][0])
        self.product_family = self.records[0][1]
        self.label1 = self.records[0][2]
        self.consumption2 = float(self.records[1][0])
        self.label2 = self.records[1][2]
        

    def get_type_consumption(self):
        self.consum_type_prodfamily_var = [self.product_family]
        self.records = exec_query_records(self.consum_type_prodfamily, self.consum_type_prodfamily_var, self.cursor)
        self.consumption_type = self.records[0][0]


    def cal_cycles(self, consumption, time):
        n_weeks_month = 365 / 12 / 7
        return consumption * self.price_kwh *  time  * n_weeks_month


    def cal_kwh(self, consumption, time):
        n_days_month = 365 / 12 
        return consumption * self.price_kwh * time * n_days_month 


    def decide_calculator(self):
        if self.consumption_type == 'hour' or self.consumption_type == 'permanent' or self.consumption_type == 'hours_week':
            self.cost_1 = self.cal_kwh(self.consumption1, self.time)
            self.cost_2 = self.cal_kwh(self.consumption2, self.time)
        else:
            self.cost_1 = self.cal_cycles(self.consumption1, self.time)
            self.cost_2 = self.cal_cycles(self.consumption2, self.time)

    
    def get_label(self):
        self.label1 = self.labelDict[self.label1]
        self.label2 = self.labelDict[self.label2]


    def return_json(self):
        self.json = {'session_id': self.session_id,
                     'label1': self.label1,
                     'consumption1': self.consumption1,
                     'Cost1': str(round(self.cost_1, 2)),
                     'label2': self.label2,
                     'consumption2': self.consumption2,
                     'Cost2': str(round(self.cost_2, 2))}
        self.json = jsonify(self.json)


    def store_data(self):    
        self.update_calculate_var = [self.brand1, self.model1, self.brand2, self.model2, str(self.time), str(self.price_kwh), str(self.current_datetime), str(self.cost_1), str(self.cost_2), self.product_family, str(self.session_id)]
        exec_query_no_records(self.update_calculate, self.update_calculate_var, self.cursor)
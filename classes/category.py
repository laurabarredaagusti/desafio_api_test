from flask import jsonify
from functions import *
from queries.queries import *

from variables import host, port, user, password, database

class Category:
    host = host
    port = port
    user = user
    password = password
    database = database 
    brand_model_product = brand_model_product
    consum_type_prodfamily = consum_type_prodfamily

    def __init__(self, category):
        self.product_category = category

        self.cursor = connect_database()
        self.get_brand_model()
        self.get_brand_list()
        self.get_equivalences()
        self.get_type_consumption()
        self.get_json()

    def get_brand_model(self):
        self.brand_model_productvar = [self.product_category]
        self.records = exec_query_records(self.brand_model_product, self.brand_model_productvar, self.cursor)

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

    def get_type_consumption(self):
        self.consum_type_prodfamilyvar = [self.product_category]
        self.records = exec_query_records(self.consum_type_prodfamily, self.consum_type_prodfamilyvar, self.cursor)
        self.consumption_type = self.records[0][0]

    def get_json(self):
        self.equiv_dic_total = {'Brand': self.brand_list,
                                'Model_by_brand' : self.equiv_dict_new,
                                'Consumption_type' : self.consumption_type}

        self.json = jsonify(self.equiv_dic_total)
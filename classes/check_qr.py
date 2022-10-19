from functions import *
from queries.queries import *
from variables import host, port, user, password, database

class CheckQr():
    host = host
    port = port
    user = user
    password = password
    database = database
    brand_model_prodfam_productid = brand_model_prodfam_productid
    update_usersearch_brandmodel = update_usersearch_brandmodel

    def __init__(self, id1, id2, session_id):
        self.productId1 = id1
        self.productId2 = id2
        self.session_id = session_id

        self.cursor = connect_database()
        self.get_brand_model_fam()
        self.filter_family()

    def get_brand_model_fam(self):
        self.brand_model_prodfam_productid_var = [self.productId1, self.productId2]
        self.records = exec_query_records(self.brand_model_prodfam_productid, self.brand_model_prodfam_productid_var, self.cursor)
        self.brand1 = self.records[0][0]
        self.model1 = self.records[0][1]
        self.product_family1 = self.records[0][2]
        self.brand2 = self.records[1][0]
        self.model2 = self.records[1][1]
        self.product_family2 = self.records[1][2]

    
    def filter_family(self):
        if self.product_family1 == self.product_family2:
            self.store_data()
            self.create_object_store()


    def store_data(self):      
        self.update_usersearch_brandmodel_var = [self.brand1, self.model1, self.brand2, self.model2, (str(self.session_id))]    
        exec_query_no_records(self.update_usersearch_brandmodel, self.update_usersearch_brandmodel_var, self.cursor)


    def create_object_store(self):
        self.result = {'Session_id': self.session_id,
                       'Brand1': self.brand1,
                       'Model1': self.model1, 
                       'Brand2': self.brand2,
                       'Model2': self.model2}
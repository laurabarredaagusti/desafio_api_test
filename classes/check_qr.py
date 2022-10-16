import psycopg2
import json

from variables import *

class Check_qr():
    host = host
    port = port
    user = user
    password = password
    database = database

    def __init__(self, id, session_id):
        self.id = id
        self.session_id = session_id

        self.connect_database()
        self.get_brand_model()
        self.check_if_available()

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
        query = '''SELECT "Brand", "Model" FROM products_id WHERE "Id" = \'''' + self.id + '''\';'''
        self.exec_query(query)

    def check_if_available(self):
        if len(self.records) > 0:
            self.brand = self.records[0][0]
            self.model = self.records[0][1]
            self.store_data()
            self.create_object_store()

    def store_data(self):        
        query = '''UPDATE user_search 
        SET 
            "Brand" = \'''' + self.brand + '''\', 
            "Model" = \'''' + self.model + '''\' WHERE
            "Session_id" = \'''' + str(self.session_id) + '''\';'''
        
        
        self.cursor.execute(query)

    def create_object_store(self):
        self.result = {'Session_id': self.session_id,
                       'Brand': self.brand,
                       'Model': self.model}
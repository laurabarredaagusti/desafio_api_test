import psycopg2
import json

from variables import *

class Check_qr():
    host = host
    port = port
    user = user
    password = password
    database = database
    store_data_path = store_data_path

    def __init__(self, id, session_id):
        self.id = id
        self.session_id = session_id

        self.connect_database()
        self.create_cursor()
        self.exec_query()
        self.check_if_available()

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
        query = '''SELECT "Brand", "Model" FROM products_id WHERE "Id" = \'''' + self.id + '''\';'''
        self.cursor.execute(query)
        self.records = self.cursor.fetchall()

    def check_if_available(self):
        if len(self.records) != 0:
            self.brand = self.records[0][0]
            self.model = self.records[0][1]
            self.create_object()
            self.read_data_json()
            self.update_json()

    def create_object(self):
        self.result = {'Brand': self.brand,
                       'Model': self.model}

    def read_data_json(self):
        with open(self.store_data_path, 'r') as j:
            self.contents = json.loads(j.read())

    def update_json(self):
        self.contents[str(self.session_id)] = self.result
        with open(self.store_data_path, 'w') as outfile:
            json.dump(self.contents, outfile)
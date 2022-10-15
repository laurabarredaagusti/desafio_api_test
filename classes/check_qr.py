import psycopg2

from variables import *

class Check_qr():
    host = host
    port = port
    user = user
    password = password
    database = database

    def __init__(self, id):
        self.id = id
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
        if len(self.records) == 0:
            self.result = 'Not available'
        else:
            self.brand = self.records[0][0]
            self.model = self.records[0][1]
            self.result = self.brand + ' ' + self.model
import uuid
import psycopg2
from variables import host, port, user, password, database

class SessionId():
    host = host
    port = port
    user = user
    password = password
    database = database 

    def __init__(self) -> None:
        self.get_id()
        self.connect_database()
        self.exec_query()

    def get_id(self):
        self.session_id = str(uuid.uuid1())

    def connect_database(self):
        self.db = psycopg2.connect(host=self.host,
                            port=self.port,
                            user=self.user,
                            password=self.password,
                            database=self.database)
        self.db.autocommit=True
        self.cursor = self.db.cursor()

    def exec_query(self):
        query = '''INSERT INTO user_search ("Session_id") VALUES (\'''' + self.session_id + '''\');'''
        self.cursor.execute(query)
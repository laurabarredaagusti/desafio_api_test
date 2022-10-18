import uuid
from functions import *
from queries.queries import *
from variables import host, port, user, password, database

class SessionId():
    host = host
    port = port
    user = user
    password = password
    database = database 
    insert_sessionid_usersearch = insert_sessionid_usersearch

    def __init__(self) -> None:
        self.get_id()
        self.cursor = connect_database()
        self.exec_query()

    def get_id(self):
        self.session_id = str(uuid.uuid1())

    def exec_query(self):
        self.insert_sessionid_usersearch_var = [self.session_id]
        exec_query_no_records(self.insert_sessionid_usersearch, self.insert_sessionid_usersearch_var, self.cursor)
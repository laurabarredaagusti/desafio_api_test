from flask import request
import psycopg2
from variables import *

def get_argument(argument):
    return request.args.get(argument, 0)

def connect_database():
        db = psycopg2.connect(host=host,
                            port=port,
                            user=user,
                            password=password,
                            database=database)
        db.autocommit=True
        return db.cursor()

def exec_query_records(query, variables, cursor):
    cursor.execute(query, variables)
    return cursor.fetchall()

def exec_query_no_records(query, variables, cursor):
    cursor.execute(query, variables)
    



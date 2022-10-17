from flask import request
import json
from datetime import date

def get_argument(argument):
    return request.args.get(argument, 0)

def read_json(path):
    with open(path, 'r') as j:
        return json.loads(j.read())

def get_current_datetime():
    today = date.today()
    return today.strftime("%d/%m/%Y")
    



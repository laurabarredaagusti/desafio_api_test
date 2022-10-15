from flask import request
import json
from datetime import date
import uuid
from classes.kwh import *
from variables import *

def get_argument(argument):
    return request.args.get(argument, 0)

def read_json(path):
    with open(path, 'r') as j:
        return json.loads(j.read())

def get_current_datetime():
    today = date.today()
    return today.strftime("%d/%m/%Y")


def check_today_price_exist():
    prices = read_json(kwh_price_path)
    current_datetime = get_current_datetime()
    if current_datetime not in prices:
        scrap = KWh()
        return scrap.price
    else:
        return prices[current_datetime], current_datetime

def get_id():
    return uuid.uuid1()

def get_stored_brand_model(id):
    data = read_json(store_data_path)
    brand = data[id]['Brand']
    model = data[id]['Model']
    return brand, model



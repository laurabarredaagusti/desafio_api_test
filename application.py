from unittest import result
from flask import Flask
from flask_cors import CORS

from classes.category import *
from classes.calculate import *
from classes.check_qr import *
from functions import *
from variables import *

application = Flask(__name__)
CORS(application)

@application.route('/')
def hello_world():
    return 'Desafio API test'

@application.route('/category', methods=['GET'])
def category():
    category = get_argument('category')
    session_id = get_id()
    if category == 0:
        return 'Missing argument'
    else:
        query = Category(category, session_id)
        return query.json

@application.route('/check_qr', methods=['GET'])
def check_qr():
    id = get_argument('id')
    session_id = get_id()
    if id == 0:
        return 'Missing argument'
    else:
        query = Check_qr(id, session_id)
        return query.result

@application.route('/calculate', methods=['GET'])
def calculate():
    session_id = get_argument('id')
    brand = get_argument('brand')
    model = get_argument('model')
    hours_day = float(get_argument('hours_day'))

    if (brand == 0 or model == 0 or hours_day == 0 or session_id == 0) and (hours_day == 0 or session_id == 0):
        return 'Missing argument'
    else:
        if brand == 0 and model == 0:
            brand, model = get_stored_brand_model(session_id)
            
        price_kwh, current_datetime = check_today_price_exist()
        calculator = Calculate(session_id, [brand, model, hours_day, price_kwh, current_datetime])
        return calculator.json

application.run()

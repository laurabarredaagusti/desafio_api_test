from flask import Flask, jsonify
from flask_cors import CORS

from classes.category import Category
from classes.calculate import Calculate
from classes.check_qr import CheckQr
from classes.session_id import SessionId
from classes.kwh import GetKWh

from functions import get_argument

from variables import API_KEY

application = Flask(__name__)

# cors_config = {'origins': []}

CORS(application)


@application.route('/')
def hello_world():
    return 'Desafio API test'


@application.route('/category', methods=['GET'])
def category():

    category = get_argument('category')
    api_key = get_argument('api_key')
    query = SessionId()

    if api_key == API_KEY:
        if category == 0:
            return 'Missing argument'
        else:
            query = Category(category, query.session_id)
            return query.json
    else:
        return 'Forbidden'


@application.route('/check_qr', methods=['GET'])
def check_qr():
    product_id = get_argument('product_id')
    api_key = get_argument('api_key')
    query = SessionId()

    if api_key == API_KEY:
        if id == 0:
            return 'Missing argument'
        else:
            query = CheckQr(product_id, query.session_id)
            return query.result
    else:
        return 'Forbidden'


@application.route('/calculate', methods=['GET'])
def calculate():

    session_id = get_argument('session_id')
    brand = get_argument('brand')
    model = get_argument('model')
    time = get_argument('time')
    api_key = get_argument('api_key')

    if api_key == API_KEY:
        if (brand == 0 or model == 0 or session_id == 0) and (time == 0 or session_id == 0):
            return 'Missing argument'
        else:   
            kwh = GetKWh()
            price_kwh = kwh.price
            current_datetime = kwh.current_date
            
            calculator = Calculate(session_id, [brand, model, time, price_kwh, current_datetime])
            return calculator.json
    else:
        return 'Forbidden'


@application.route('/advanced', methods=['GET'])
def advanced():
    session_id = get_argument('session_id')
    months = get_argument('months')
    price = get_argument('price')
    api_key = get_argument('api_key')

    if api_key == API_KEY:
        if session_id == 0 or months == 0 or price == 0:
            return 'Missing arguments'
        
        else:
            dict_for_full = {'amortization_year' : 3,
                    'end_year' : 5,
                    'end_value' : 300}
            return jsonify(dict_for_full)
    else:
        return 'Forbidden'

application.run()

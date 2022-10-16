from unittest import result
from flask import Flask, jsonify
# from flask_cors import CORS

from classes.category import *
from classes.calculate import *
from classes.check_qr import *
from classes.session_id import *
from classes.kwh import *

from functions import *
from variables import *

application = Flask(__name__)
# CORS(application)


@application.route('/')
def hello_world():
    return 'Desafio API test'


@application.route('/category', methods=['GET'])
def category():

    category = get_argument('category')
    query = Session_id()

    if category == 0:
        return 'Missing argument'
    else:
        query = Category(category, query.session_id)
        return query.json


@application.route('/check_qr', methods=['GET'])
def check_qr():
    id = get_argument('id')
    query = Session_id()

    if id == 0:
        return 'Missing argument'
    else:
        query = Check_qr(id, query.session_id)
        return query.result


@application.route('/calculate', methods=['GET'])
def calculate():

    session_id = get_argument('session_id')
    brand = get_argument('brand')
    model = get_argument('model')
    hours_day = get_argument('hours_day')

    if (brand == 0 or model == 0 or hours_day == 0 or session_id == 0) and (hours_day == 0 or session_id == 0):
        return 'Missing argument'
    else:   
        kwh = Get_KWh()
        price_kwh = kwh.price
        current_datetime = kwh.current_date
        
        calculator = Calculate(session_id, [brand, model, hours_day, price_kwh, current_datetime])
        return calculator.json


@application.route('/advanced', methods=['GET'])
def advanced():
    session_id = get_argument('session_id')
    months = get_argument('months')
    price = get_argument('price')

    if session_id == 0 or months == 0 or price == 0:
        return 'Missing arguments'
    
    else:
        dict = {'cross_year' : 3,
                'end_year' : 5,
                'end_value' : 300}
        return jsonify(dict)

application.run()

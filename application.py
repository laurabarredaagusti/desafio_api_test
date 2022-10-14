from flask import Flask, request
from flask_cors import CORS

from classes.category import *
from classes.kwh import *
from functions import *

application = Flask(__name__)
CORS(application)

@application.route('/')
def hello_world():
    return 'Desafio API test'

@application.route('/category', methods=['GET'])
def category():
    category = get_argument('category')
    if category == None:
        return 'Missing argument'
    else:
        query = Category(category)
        return query.json

@application.route('/calculate', methods=['GET'])
def calculate():
    brand = get_argument('brand')
    model = get_argument('model')
    price = get_argument('price')
    hours_month = float(get_argument('hours_month'))
    hours_day = float(get_argument('hours_day'))
    if brand == None or model == None or hours_month == None or hours_day == None:
        return 'Missing argument'
    else:
        scrap = KWh()
        price_kwh = float(scrap.price)
        cost =  price_kwh * hours_month * hours_day

        dict = {'Cost': str(cost)}

        dict_json = jsonify(dict)

        return dict_json

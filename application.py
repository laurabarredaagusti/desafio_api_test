from flask import Flask
from flask_cors import CORS

from classes.advanced_calculate import AdvancedCalculate
from classes.category import Category
from classes.calculate import Calculate
from classes.check_qr import CheckQr
from classes.session_id import SessionId
from classes.kwh import GetKWh

from functions import get_argument

from variables import API_KEY

application = Flask(__name__)
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
    productId1 = get_argument('productId1')
    productId2 = get_argument('productId2')
    api_key = get_argument('api_key')
    query = SessionId()

    if api_key == API_KEY:
        if productId1 == 0 or productId2 == 0:
            return 'Missing argument'
        else:
            query = CheckQr(productId1, productId2, query.session_id)
            return query.result
    else:
        return 'Forbidden'


@application.route('/calculate', methods=['GET'])
def calculate():

    session_id = get_argument('session_id')
    brand1 = get_argument('brand1')
    model1 = get_argument('model1')
    brand2 = get_argument('brand2')
    model2 = get_argument('model2')
    time = get_argument('time')
    api_key = get_argument('api_key')

    if api_key == API_KEY:
        if (brand1 == 0 or model1 == 0 or brand2 == 0 or model2 == 0  or session_id == 0 or time == 0) and (session_id == 0 or time == 0):
            return 'Missing argument'

        elif brand1 == brand2 and model1 == model2:
            return 'Same product'

        else:   
            kwh = GetKWh()
            price_kwh = kwh.price
            current_datetime = kwh.current_date
            
            calculator = Calculate(session_id, [brand1, model1, brand2, model2, time, price_kwh, current_datetime])
            return calculator.json
    else:
        return 'Forbidden'


@application.route('/advanced', methods=['GET'])
def advanced():
    sessionId = get_argument('session_id')
    months = get_argument('months')
    price1 = get_argument('price1')
    price2 = get_argument('price2')
    api_key = get_argument('api_key')

    if api_key == API_KEY:
        if sessionId == 0 or months == 0 or price1 == 0 or price2 == 0:
            return 'Missing arguments'
        else:
            query = AdvancedCalculate(months, price1, price2, sessionId)
            return query.result_obj
    else:
        return 'Forbidden'


if __name__ == '__main__':
    application.run(threaded=True, port=5000)

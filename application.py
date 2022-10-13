from flask import Flask, request

application = Flask(__name__)

@application.route('/')
def hello_world():
    return 'Desafio API test'

@application.route('/result', methods=['GET'])
def result():
    brand = request.args.get('brand', 'me')
    result = 'The brand is ' + brand
    return result

@application.route('/category', methods=['GET'])
def result():
    category = request.args.get('category', 'me')
    result = 'The category is ' + category
    return result
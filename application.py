from flask import Flask, request
from flask_cors import CORS
from classes.category import *
from functions import *

application = Flask(__name__)
CORS(application)

@application.route('/')
def hello_world():
    return 'Desafio API test'

@application.route('/category', methods=['GET'])
def result():
    category = get_argument('category')
    if category == None:
        return 'Missing argument'
    else:
        query = Category(category)
        return query.json

application.run()
from flask import Flask

application = Flask(__name__)

@application.route('/')
def hello_world():
    return 'Desafio API test'
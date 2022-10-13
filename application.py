from flask import Flask, request, jsonify
import psycopg2

application = Flask(__name__)

@application.route('/')
def hello_world():
    return 'Desafio API test'

@application.route('/category', methods=['GET'])
def result():
    category = request.args.get('category', None)

    db = psycopg2.connect(host='desafio-tripulaciones.c5mpkjhryqaz.us-east-2.rds.amazonaws.com',
                            port=5432,
                            user='postgres',
                            password='desafiotripulaciones',
                            database='etiqueta_energetica')

    db.autocommit=True

    cursor = db.cursor()

    select_query = 'SELECT "Brand", "Model" FROM ' + category

    cursor.execute(select_query)

    records = cursor.fetchall()

    list_brand = [elem[0] for elem in records]
    list_model = [elem[1] for elem in records]

    dict = {'Brand': list_brand,
            'Model' : list_model}

    return jsonify(dict)
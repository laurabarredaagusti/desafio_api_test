host='desafio-tripulaciones.c5mpkjhryqaz.us-east-2.rds.amazonaws.com'
port=5432
user='postgres'
password='desafiotripulaciones'
database='etiqueta_energetica'

kwh_price_path = 'files/kwh_price.json'
store_data_path = 'files/checked_models.json'

store_data = ['brand', 'model', 'hours_day', 'price_kwh', 'current_datetime', 'cost']
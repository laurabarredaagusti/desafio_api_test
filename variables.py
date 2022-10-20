host='desafio-tripulaciones.c5mpkjhryqaz.us-east-2.rds.amazonaws.com'
port=5432
user='postgres'
password='desafiotripulaciones'
database='etiqueta_energetica'

kwh_price_path = 'files/kwh_price.json'

API_KEY = '923fc55c-57d8-4147-bf38-ef23d7e707ad'

labelDict = {'APPP': 'https://eprel.ec.europa.eu/assets/images/label/thumbnails/A-Left-DarkGreen-WithAGScale.png',
             'APP': 'https://eprel.ec.europa.eu/assets/images/label/thumbnails/A-Left-DarkGreen-WithAGScale.png',
             'AP': 'https://eprel.ec.europa.eu/assets/images/label/thumbnails/A-Left-DarkGreen-WithAGScale.png',
             'A': 'https://eprel.ec.europa.eu/assets/images/label/thumbnails/A-Left-DarkGreen-WithAGScale.png',
             'B': 'https://eprel.ec.europa.eu/assets/images/label/thumbnails/B-Left-MediumGreen-WithAGScale.png',
             'C': 'https://eprel.ec.europa.eu/assets/images/label/thumbnails/C-Left-LightGreen-WithAGScale.png',
             'D': 'https://eprel.ec.europa.eu/assets/images/label/thumbnails/D-Left-Yellow-WithAGScale.png',
             'E': 'https://eprel.ec.europa.eu/assets/images/label/thumbnails/E-Left-LightOrange-WithAGScale.png',
             'F': 'https://eprel.ec.europa.eu/assets/images/label/thumbnails/F-Left-DarkOrange-WithAGScale.png',
             'G': 'https://eprel.ec.europa.eu/assets/images/label/thumbnails/G-Left-Red-WithAGScale.png'}

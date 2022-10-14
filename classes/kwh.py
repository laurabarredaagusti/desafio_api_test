from bs4 import BeautifulSoup as bs
# import requests

class KWh:
    url = 'https://tarifaluzhora.es/'
    def __init__(self):
        pass
        # self.create_soup()
        # self.get_price()
    
    # def create_soup(self):
    #     response = requests.get(self.url)
    #     html = response.content
    #     self.soup = bs(html, "lxml")
    
    # def get_price(self):
    #     self.price = float(self.soup.find('span', class_='main_text').text[:-2])
        self.price = str(self.price)
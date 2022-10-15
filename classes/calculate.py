from flask import jsonify
import json
from variables import *

class Calculate:
    store_data_path = store_data_path
    def __init__(self, arguments_list):

        self.arguments_list = arguments_list
        self.price = float(arguments_list[2])
        self.hours_month = float(arguments_list[3])
        self.hours_day = float(arguments_list[4])
        self.current_datetime = arguments_list[5]
        
        self.calculate()
        self.get_dict()
        self.get_json()
        self.read_data_json()
        self.store_data_dict()
        self.update_json()

    def calculate(self):
        self.cost = self.price * self.hours_month * self.hours_day

    def get_dict(self):
        self.dict = {'Cost': str(self.cost)}

    def get_json(self):
        self.json = jsonify(self.dict)

    def read_data_json(self):
        with open(self.store_data_path, 'r') as j:
            self.contents = json.loads(j.read())

    def store_data_dict(self):
        self.data_dict = {}
        for index, data in enumerate(store_data):
            self.data_dict[data] = self.arguments_list[index]

    def update_json(self):
        self.contents[self.current_datetime] = self.data_dict
        with open(self.store_data_path, 'w') as outfile:
            json.dump(self.contents, outfile)


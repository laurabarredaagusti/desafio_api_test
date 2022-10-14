from flask import jsonify

class Calculate:
    def __init__(self, price, hours_month, hours_day):
        self.price = float(price)
        self.hours_month = hours_month
        self.hours_day = hours_day
        pass

    def calculate(self):
        self.cost = self.price * self.hours_month * self.hours_day

    def get_dict(self):
        self.dict = {'Cost': str(self.cost)}

    def get_json(self):
        self.json = jsonify(self.dict)

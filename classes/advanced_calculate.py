from functions import *
from queries.queries import *

class AdvancedCalculate():

    cost_usersearch = cost_usersearch
    update_usersearch_advanced = update_usersearch_advanced

    def __init__(self, months, price1, price2, sessionId):
        self.months = int(months)
        self.price1 = float(price1)
        self.price2 = float(price2)
        self.sessionId = sessionId

        self.cursor = connect_database()
        self.get_cost()
        self.calculate_am()
        self.get_object()
        self.store_data()


    def get_cost(self):
        self.cost_usersearch_var = [self.sessionId]
        self.records = exec_query_records(self.cost_usersearch, self.cost_usersearch_var, self.cursor)
        self.cost1 = float(self.records[0][0])
        self.cost2 = float(self.records[0][1])

    def init_point(self):
        self.initPoint1 = (0, self.price1)
        self.initPoint2 = (0, self.price2)

    def crossing_year(self):
        if self.price1 == self.price2 and self.cost1 == self.cost2:
            self.crossingYear = (self.price1 - self.price2) * (1/self.months)
        else:
            self.crossingYear = (self.price1 - self.price2) * (1 / (self.cost2 - self.cost1)) * (1 / self.months)

    def crossing_point(self):
        self.crossingCost = self.price2 + self.cost2 * self.crossingYear * self.months
        self.crossingPoint = (self.crossingYear, self.crossingCost)

    def end_year(self):
        if self.crossingYear > 0:
            self.totalYear = self.crossingYear + 2
        else:
            self.totalYear = 5

    def end_point(self):
        self.endValue1 = self.price1 + self.cost1 * (self.crossingYear + 2) * self.months
        self.endValue2 = self.price2 + self.cost2 * (self.crossingYear + 2) * self.months
        self.endPoint1 = (self.crossingYear + 2 , self.endValue1)
        self.endPoint2 = (self.crossingYear + 2, self.endValue2)

    def calculate_am(self):
        self.init_point()
        self.crossing_year()
        self.crossing_point()
        self.end_point()

    def get_object(self):
        self.result_obj = {'CrossingYear': self.crossingYear,
                           'crossingCost': self.crossingCost,
                           'Total_years': self.totalYear,
                           'EndValue1': self.endValue1,
                           'EndValue2': self.endValue2,
                           'brand1': 'brand1',
                           'brand2': 'brand2',
                           'model1': 'model1',
                           'model2': 'model2'}

    def store_data(self):
        self.update_usersearch_advanced_var = [self.crossingYear, self.crossingCost, self.sessionId]
        exec_query_no_records(self.update_usersearch_advanced, self.update_usersearch_advanced_var, self.cursor)

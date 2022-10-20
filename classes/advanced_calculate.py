from functions import *
from queries.queries import *
import numpy as np

class AdvancedCalculate():

    cost_usersearch = cost_usersearch
    update_usersearch_advanced = update_usersearch_advanced
    brands_models_usersearch = brands_models_usersearch

    def __init__(self, months, price1, price2, sessionId):
        self.months = int(months)
        self.price1 = float(price1)
        self.price2 = float(price2)
        self.sessionId = sessionId

        self.cursor = connect_database()
        self.get_cost()
        self.calculate_am()
        self.get_brand_model()
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

    def calculate_am(self):
        self.init_point()
        if (self.price1 != self.price2) and (self.cost1 != self.cost2) and ((self.price1 > self.price2 and self.cost1 < self.cost2) or (self.price1 < self.price2 and self.cost1 > self.cost2)):
            self.crossingYear = (self.price1 - self.price2) * (1 / (self.cost2 - self.cost1)) * (1 / self.months)
            self.crossingCost = self.price2 + self.cost2 * self.crossingYear * self.months
            self.crossingPoint = (abs(self.crossingYear), self.crossingCost) 
            
            # SI SE CRUZAN EN MÁS DE 15 AÑOS
            if (abs(self.crossingYear)) > 15:
                self.totalYear = 10 
                self.endValue1 = self.price1 + self.cost1 * self.totalYear * self.months
                self.endValue2 = self.price2 + self.cost2 * self.totalYear * self.months
                self.endPoint1 = (self.totalYear, self.endValue1)
                self.endPoint2 = (self.totalYear, self.endValue2)
            else:   
                self.totalYear =  self.crossingYear + 5
                self.endValue1 = self.price1 + self.cost1 * self.totalYear * self.months
                self.endValue2 = self.price2 + self.cost2 * self.totalYear * self.months
                self.endPoint1 = self.totalYear, self.endValue1
                self.endPoint2 = (self.totalYear, self.endValue2)
        else:
            self.crossingYear = 0
            self.crossingCost = 0
            self.crossingPoint = (self.crossingYear, self.crossingCost) 
            self.totalYear = 5
            self.endValue1 = self.price1 + self.cost1 * self.totalYear * self.months
            self.endValue2 = self.price2 + self.cost2 * self.totalYear * self.months
            self.endPoint1 = (self.totalYear, self.endValue1)
            self.endPoint2 = (self.totalYear, self.endValue2) 

    def get_brand_model(self):
        self.brands_models_usersearch_var = [self.sessionId]
        self.records = exec_query_records(self.brands_models_usersearch, self.brands_models_usersearch_var, self.cursor)
        self.brand1 = self.records[0][0].title()
        self.model1 = self.records[0][1].upper()
        self.brand2 = self.records[0][2].title()
        self.model2 = self.records[0][3].upper()

    def get_object(self):
        self.difference = [self.endValue1, self.endValue2]
        self.difference.sort()
        self.difference = np.diff(self.difference)

        self.result_obj = {'CrossingYear': self.crossingYear,
                           'crossingCost': self.crossingCost,
                           'Total_years': round(self.totalYear, 1),
                           'EndValue1': self.endValue1,
                           'EndValue2': self.endValue2,
                           'brand1': self.brand1,
                           'brand2': self.brand2,
                           'model1': self.model1,
                           'model2': self.model2,
                           'difference': self.difference[0]}

    def store_data(self):
        self.update_usersearch_advanced_var = [self.crossingYear, self.crossingCost, self.sessionId]
        exec_query_no_records(self.update_usersearch_advanced, self.update_usersearch_advanced_var, self.cursor)

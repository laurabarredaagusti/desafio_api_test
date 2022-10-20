from functions import *
from queries.queries import *

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

    # def crossing_year(self):
    #     if self.cost1 == self.cost2:
    #         self.crossingYear = 0
    #     else:
    #         self.crossingYear = (self.price1 - self.price2) * (1 / (self.cost2 - self.cost1)) * (1 / self.months)

    # def crossing_point(self):
    #     self.crossingCost = self.price2 + self.cost2 * self.crossingYear * self.months
    #     self.crossingPoint = (self.crossingYear, self.crossingCost)

    # def end_year(self):
    #     if self.crossingYear > 0:
    #         self.totalYear = self.crossingYear * 1.2
    #     else:
    #         self.totalYear = 5

    # def end_point(self):
    #     if (self.price1 > self.price2 and self.cost1 > self.cost2) or (self.price1 < self.price2 and self.cost1 < self.price2):
    #         self.endValue1 = abs(self.price1 + self.cost1 * (self.crossingYear + 5) * self.months)
    #         self.endValue2 = abs(self.price2 + self.cost2 * (self.crossingYear + 5) * self.months)
    #         self.endPoint1 = (5, self.endValue1)
    #         self.endPoint2 = (5, self.endValue2)
    #     else:
    #         self.endValue1 = self.price1 + self.cost1 * (self.crossingYear + 2) * self.months
    #         self.endValue2 = self.price2 + self.cost2 * (self.crossingYear + 2) * self.months
    #         self.endPoint1 = (self.crossingYear + 2 , self.endValue1)
    #         self.endPoint2 = (self.crossingYear + 2, self.endValue2)

    def calculate_am(self):
        self.init_point()
        # self.crossing_year()
        # self.crossing_point()
        # self.end_year()
        # self.end_point()

        cond1 = self.price1 != self.price2
        cond2 = self.cost1 != self.cost2
        cond3 = (self.price1 > self.price2 and self.cost1 < self.cost2)
        cond4 = (self.price1 < self.price2 and self.cost1 > self.cost2)
        cond5 = (cond3 or cond4)

        if cond1 and cond2 and cond5:
            self.crossingYear = (self.price1 - self.price2) * (1 / (self.cost1 + self.cost2)) * (1 / self.months)
            self.crossingCost = self.price2 + self.cost2 * self.crossingYear * self.months
            self.crossingPoint = (abs(self.crossingYear), self.crossingCost) 
            
            # SI SE CRUZAN EN MÁS DE 15 AÑOS
            if (abs(self.crossingYear))>15:
                self.totalYear = 15
                self.endValue1 = self.price1 + self.cost1 * (15) * self.months
                self.endValue2 = self.price2 + self.cost2 * (15) * self.months
                self.endPoint1 = (self.totalYear, self.endValue1)
                self.endPoint2 = (self.totalYear, self.endValue2)
            else:   
                self.totalYear =  self.crossingYear * 1.3
                self.endValue1 = self.price1 + self.cost1 * (self.crossingYear * 1.3) * self.months
                self.endValue2 = self.price2 + self.cost2 * (self.crossingYear * 1.3) * self.months
                self.endPoint1 = self.totalYear, self.endValue1
                self.endPoint2 = (self.totalYear, self.endValue2)

        else:
            self.crossingPoint = (0,0) 
            self.totalYear = 5
            self.endValue1 = self.price1 + self.cost1 * (5) * self.months
            self.endValue2 = self.price2 + self.cost2 * (5) * self.months
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
        self.result_obj = {'CrossingYear': self.crossingYear,
                           'crossingCost': self.crossingCost,
                           'Total_years': self.totalYear,
                           'EndValue1': self.endValue1,
                           'EndValue2': self.endValue2,
                           'brand1': self.brand1,
                           'brand2': self.brand2,
                           'model1': self.model1,
                           'model2': self.model2}

    def store_data(self):
        self.update_usersearch_advanced_var = [self.crossingYear, self.crossingCost, self.sessionId]
        exec_query_no_records(self.update_usersearch_advanced, self.update_usersearch_advanced_var, self.cursor)

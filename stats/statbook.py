import numpy as np
from scipy.stats import norm


class StatBook(object):

    def __init__(self, tests, positives, population, testing_sites):

        self.tests = tests

        self.positives = positives

        self.population = population
        
        self.testing_sites = testing_sites

        self.prop_positive = positives / tests

        self.calculate()

    @staticmethod
    def proportion_variance(p):

        return p*(1-p)

    @staticmethod
    def finite_population_correction(tests, population):

        numerator = population - tests

        denominator = population - 1

        return numerator/denominator
    
    @staticmethod
    def normalize(x):
        
        return (x - np.min(x)) / (np.max(x) - np.min(x))

    def _std_error_fpc(self):

        var = self.proportion_variance(self.prop_positive)

        self.fpc = self.finite_population_correction(self.tests, self.population)

        self.std_err_fpc = np.sqrt((var/self.tests)*self.fpc)

    def _confidence_interval_fpc(self):

        confidence = 1.96*self.std_err_fpc

        self.lower_interval = self.prop_positive - confidence

        self.upper_interval = self.prop_positive + confidence
    
    def _score(self):
        
        positive = self.prop_positive
        
        uncertainty = self.normalize(self.std_err_fpc)
        
        pop = self.normalize(self.population)
        
        testing_sites = self.normalize(self.testing_sites)
        
        norm_score = self.normalize(positive + uncertainty + pop - testing_sites )
        
        self.score = norm_score
        
    def get_score(self):
        
        return self.score        

    def calculate(self):

        self._std_error_fpc()

        self._confidence_interval_fpc()
        
        self._score()

    def get_conf_interval(self):

        return self.lower_interval, self.upper_interval

    def get_fpc(self):

        return self.fpc


# Used to tranform the location column in our testing site data into a format
# that folium can use
def pull_loc(point):

    if type(point) == str:

        point_sub = point[7:].split(' ')

        lon = float(point_sub[0])

        lat = float(point_sub[1].split(')')[0])

    else:

        lat, lon = None, None

    return (lat, lon)

import numpy as np
from scipy.stats import norm


class StatBook(object):

    def __init__(self, tests, positives, population):

        self.tests = tests

        self.positives = positives

        self.population = population

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

    def _std_error_fpc(self):

        var = self.proportion_variance(self.prop_positive)

        self.fpc = self.finite_population_correction(self.tests, self.population)

        self.std_err_fpc = np.sqrt((var/self.tests)*self.fpc)

    def _confidence_interval_fpc(self):

        confidence = 1.96*self.std_err_fpc

        self.lower_interval = self.prop_positive - confidence

        self.upper_interval = self.prop_positive + confidence

    def calculate(self):

        self._std_error_fpc()

        self._confidence_interval_fpc()

    def get_conf_interval(self):

        return self.lower_interval, self.upper_interval

    def get_fpc(self):

        return self.fpc

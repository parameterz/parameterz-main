#!/usr/bin/env python

from __future__ import division
import math

required = ['bsa']
bsaMethod = 'Dubois'
constraints = {'age': [0, 20]}

name = 'Olivieri et al., JASE 2009'
description = 'BSA-adjusted z-scores for the proximal coronary arteries.'
detail = '''Z-Scores of the left main coronary artery (LMCA), left anterior
descending (LAD), and right coronary artery (RCA) using an allometric equation
derived from 432 normal patients, aged 0 - 20 years. Data from investigators
at CNMC, Washington, DC.
'''
critique = {
    'model': 'Log-log model with BSA',
    'subjects': 432,
    'heterosc': True,
    'residual_assoc': False,
    'residual_heterosc': False,
    'distribution': False
}

year = '2009'
citation = {
    'title': '''Coronary artery Z score regression equations and
	calculators derived from a large heterogeneous population of
	children undergoing echocardiography.''',
    'authors': 'Olivieri L, Arling B, Friberg M, Sable C.',
    'journal': 'J Am Soc Echocardiogr. 2009 Feb;22(2):159-64.',
    'url': 'http://www.ncbi.nlm.nih.gov/pubmed/19084373'
}


class Base(object):
    '''
	This is the base class for the Olivieri/JASE coronary arteries.
		The form of these equations is:
		    y = mx + b
		    where x is log(bsa)
		    MSE is used for the 'sd'
		    
	'''

    def __init__(self, data, pt, limit):
        self.source = name
        self.citation = citation
        self.siteName = data['name']
        self.refName = 'olivieri_jase_2009'
        self.slope = data['slope']
        self.intercept = data['intercept']
        self.mse = math.sqrt(data['mse'])  # = "rmse"
        self.limit = limit
        self.bsaMethod = bsaMethod
        self.bsa = pt.bsa(bsaMethod)
        self.score = float(getattr(pt, data['name']))
        # chart stuff
        self.chartData = True
        self.bsaData = [x * 0.1 for x in range(1, 21)]
        self.chartXAxisLabel = 'BSA'
        self.myData = ([[self.bsa, self.score]])  # plot data
        self.constraints = constraints
        self.critique = critique

    def _mean(self, bsa):
        return self.slope * math.log(bsa) + self.intercept

    def mean(self):
        return math.exp(self._mean(self.bsa)) * 10

    def zscore(self):
        try:
            return (math.log(self.score / 10) - self._mean(self.bsa)) / self.mse
        except:
            return None  # property of object 'pt' does not exist

    def uln(self):
        return math.exp(self._mean(self.bsa) + self.limit * self.mse) * 10

    def lln(self):
        return math.exp(self._mean(self.bsa) - self.limit * self.mse) * 10

    def chart_uln(self):
        return ([[x, 10 * math.exp(self.limit * self.mse + self._mean(x))] for x in self.bsaData])

    def chart_lln(self):
        return ([[x, 10 * math.exp(-self.limit * self.mse + self._mean(x))] for x in self.bsaData])

    def chart_mean(self):
        return [[x, 10 * math.exp(self._mean(x))] for x in self.bsaData]


#
# individual site data 
#

lmca = {'name': 'lmca', 'intercept': -1.31625, 'slope': 0.37442, 'mse': 0.028467}
lad = {'name': 'lad', 'intercept': -1.50927, 'slope': 0.41164, 'mse': 0.033031}
prox_rca = {'name': 'prox_rca', 'intercept': -1.46115, 'slope': 0.37870, 'mse': 0.040172}

sites = [
    'lmca',
    'lad',
    'prox_rca'
]

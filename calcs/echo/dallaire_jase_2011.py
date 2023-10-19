#!/usr/bin/env python

from __future__ import division
import math

required = ['bsa']
bsaMethod = 'Haycock'
constraints = {'age': [0.16, 18], 'bsa': [0.08, 2.72]}

name = 'Dallaire and Dahdah, JASE 2011'
description = 'BSA-adjusted z-scores for the coronary arteries.'

detail = '''BSA-adjusted z-scores for the coronary arteries. Coronary segments include
the circumflex and distal right coronary artery in addition to the usual
proximal segments (LMCA, LAD, RCA). Based on data from over 1,000 infants,
children, and adolescents seen in Montreal, Quebec, Canada.
Particular attention was paid to ensuring the data conforms to a normal
distribution&mdash; an essential point for properly interpreting z-score results.
'''

critique = {
    'model': 'linear with square root of BSA (allometric model)',
    'subjects': 1033,
    'heterosc': True,
    'residual_assoc': True,
    'distribution': True,
    'residual_heterosc': True
}

year = '2011'
citation = {
    'title': '''New equations and a critical appraisal of coronary artery
	Z scores in healthy children.''',
    'authors': 'Dallaire F, Dahdah N.',
    'journal': 'J Am Soc Echocardiogr. 2011 Jan;24(1):60-74.',
    'url': 'http://www.ncbi.nlm.nih.gov/pubmed/21074965'
}


class Base(object):
    '''
	This is the base class for the Montreal data:
		The form of these equations is:
		    y = m*x + b
		    where x = BSA^0.5
	'''

    def __init__(self, data, pt, limit):
        self.source = name
        self.citation = citation
        self.siteName = data['name']
        self.refName = 'dallaire_jase_2011'
        self.a1 = data['a1']
        self.b1 = data['b1']
        self.a2 = data['a2']
        self.b2 = data['b2']
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
        return self.a1 + self.b1 * math.sqrt(bsa)

    def mean(self):
        return self._mean(self.bsa)

    def sd(self, bsa):
        return self.a2 + self.b2 * math.sqrt(bsa)

    def zscore(self):
        try:
            return (self.score - self._mean(self.bsa)) / self.sd(self.bsa)
        except:
            return None  # property of object 'pt' does not exist

    def uln(self):
        return self.mean() + self.limit * self.sd(self.bsa)

    def lln(self):
        return self.mean() - self.limit * self.sd(self.bsa)

    def chart_uln(self):
        return ([[x, (self.limit * self.sd(x) + self._mean(x))] for x in self.bsaData])

    def chart_lln(self):
        return ([[x, (-self.limit * self.sd(x) + self._mean(x))] for x in self.bsaData])

	def chart_mean(self):
		return [[x, self._mean(x)] for x in self.bsaData]


#
# individual site data 
#

lmca = {'name': 'lmca', 'a1': -0.1817, 'b1': 2.9238, 'a2': 0.1801, 'b2': 0.2530}
lad = {'name': 'lad', 'a1': -0.1502, 'b1': 2.2672, 'a2': 0.1709, 'b2': 0.2293}
circ = {'name': 'circ', 'a1': -0.2716, 'b1': 2.3458, 'a2': 0.1142, 'b2': 0.3423}
prox_rca = {'name': 'prox_rca', 'a1': -0.3039, 'b1': 2.7521, 'a2': 0.1626, 'b2': 0.2881}
mid_rca = {'name': 'mid_rca', 'a1': -0.3060, 'b1': 2.4078, 'a2': 0.1324, 'b2': 0.3259}
dist_rca = {'name': 'dist_rca', 'a1': -0.3185, 'b1': 2.3295, 'a2': 0.1099, 'b2': 0.3198}

sites = [
    'lmca',
    'lad',
    'circ',
    'prox_rca',
    'mid_rca',
    'dist_rca'
]

#!/usr/bin/env python

from __future__ import division
import math

required = ['bsa']
bsaMethod = 'Boyd'
constraints = {'age': [0, 17.25], 'bsa': [0.1, 1.9]}

name = 'Daubeney et al., Cardiol Young 1999'
description = 'BSA-adjusted z-scores for cardiac structures.'
detail = '''Z scores of cardiac structures including the mitral valve,
aortic valve, pulmonary arteries, etc. Regression equations were
derived relating cardiac dimensions to the size of the body using a
population of 125 normal infants and children.
From the Wessex Cardiothoracic Unit, Southampton General Hospital, UK.
'''

critique ={
  'model': 'log-log with BSA',
  'subjects': 125,
  'heterosc': False,
  'residual_assoc': False,
  'residual_heterosc': False,
  'distribution': False,
  'source': 'parameterz'
}

year = '1999'
citation = {
	'title': '''Relationship of the dimension of cardiac structures to
	body size: an echocardiographic study in normal infants and children.''',
	'authors': 'Daubeney PE, Blackstone EH, Weintraub RG, Slavik Z, Scanlon J, Webber SA.',
	'journal': 'Cardiol Young. 1999 Jul;9(4):402-10.',
	'url': 'http://www.ncbi.nlm.nih.gov/pubmed/10476831'
}

class Base(object):
	'''
	This is the base class for the Daubeney/Wessex data.
		The form of these equations is:
		    y = mx + b
		    where x is log(bsa)
		    MSE is used for the 'sd'
		    
	'''

	def __init__(self, data, pt, limit ):
		self.source = name
		self.citation = citation
		self.siteName = data['name']
		self.refName = 'daubeney_cardyoung_1999'
		self.slope = data['slope']
		self.intercept = data['intercept']
		self.mse = data['mse']
		self.limit = limit
		self.bsaMethod = bsaMethod
		self.bsa = pt.bsa(bsaMethod)
		self.score = float(getattr(pt, data['name']))
		#chart stuff
		self.chartData = True
		self.bsaData = [x * 0.1 for x in range(1, 21)]
		self.chartXAxisLabel = 'BSA'
		self.myData = ( [[self.bsa, self.score]] )#plot data
		self.constraints = constraints
		self.critique = critique


	def _mean(self, bsa):
		return self.slope * math.log( bsa ) + self.intercept
		
	def mean(self):
		return math.exp( self._mean(self.bsa) ) * 10
	
	def zscore(self):
		try:
		    return ( math.log( self.score / 10 ) - self._mean(self.bsa) ) / self.mse
		except:
		    return None #property of object 'pt' does not exist
	
	def uln(self):
		return math.exp( self._mean(self.bsa) + self.limit * self.mse ) * 10
	
	def lln(self):
		return math.exp( self._mean(self.bsa) - self.limit * self.mse ) * 10

	def chart_uln(self):
		return ( [[x, 10 * math.exp( self.limit * self.mse + self._mean(x) )] for x in self.bsaData] )
	def chart_lln(self):
		return ( [[x, 10 * math.exp( -self.limit * self.mse + self._mean(x) )] for x in self.bsaData] )

# 
# individual site data 
#

tvd_l = { "name": "tvd_l", "slope": 0.4945, "intercept": 1.084, "mse": 0.08121 }
rv_in = { "name": "rv_in", "slope": 0.4962, "intercept": 1.823, "mse": 0.10860 }
rv_out = { "name": "rv_out", "slope": 0.6185, "intercept": 1.943, "mse": 0.10090 }
rv_area = { "name": "rv_area", "slope": 0.9566, "intercept": 2.795, "mse": 0.17530 }
pv = { "name": "pv", "slope": 0.5028, "intercept": 0.637, "mse": 0.11430 }
mpa = { "name": "mpa", "slope": 0.4941, "intercept": 0.607, "mse": 0.14300 }
rpa = { "name": "rpa", "slope": 0.5495, "intercept": 0.140, "mse": 0.12940 }
lpa = { "name": "lpa", "slope": 0.6039, "intercept": 0.202, "mse": 0.14460 }
mvd_ap = { "name": "mvd_ap", "slope": 0.5022, "intercept": 0.945, "mse": 0.09403 }
mvd_l = { "name": "mvd_l", "slope": 0.4658, "intercept": 0.965, "mse": 0.09167 }
lv_in = { "name": "lv_in", "slope": 0.4936, "intercept": 1.893, "mse": 0.09847 }
lv_area = { "name": "lv_area", "slope": 1.0200, "intercept": 3.141, "mse": 0.18060 }
aov = { "name": "aov", "slope": 0.5347, "intercept": 0.518, "mse": 0.06726 }
sov = { "name": "sov", "slope": 0.5082, "intercept": 0.722, "mse": 0.07284 }
stj = { "name": "stj", "slope": 0.5490, "intercept": 0.542, "mse": 0.08656 }

sites = [
	'tvd_l',
	#'rv_in',
	#'rv_out',
	#'rv_area',
	'pv',
	'mpa',
	'rpa',
	'lpa',
	'mvd_ap',
	'mvd_l',
	#'lv_in',
	#'lv_area',
	'aov',
	'sov',
	'stj'
]


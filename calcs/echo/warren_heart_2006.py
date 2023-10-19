#!/usr/bin/env python

from __future__ import division
import math

required = ['bsa']
bsaMethod = 'Boyd'
constraints = {'age': [0, 18], 'bsa': [0.25, 2.3]}

name = 'Warren et al., Heart 2006'
description = 'BSA-adjusted z-scores for the aortic valve and root; Halifax data'
detail = '''Calculate BSA-adjusted z-scores of the ascending aorta and aortic root using data
published in 2006 from Halifax, Nova Scotia. Per the authors:
>Measurements were made in systole... in the parasternal long axis...
from inner edge to inner edge. The ascending aorta was measured at the level
of the right pulmonary artery.
'''
critique = {
  'model': 'log-log with BSA',
  'subjects': 88,
  'heterosc': False,
  'residual_assoc': False,
  'residual_heterosc': False,
  'distribution': False,
  'source': 'parameterz'
}

year = '2006'
citation = {
	'title': '''Dilatation of the ascending aorta in paediatric patients
	with bicuspid aortic valve: frequency, rate of progression
	and risk factors. ''',
	'authors': 'Warren AE, Boyd ML, O\'Connell C, Dodds L.',
	'journal': 'Heart. 2006 Oct;92(10):1496-500.',
	'url': 'http://www.ncbi.nlm.nih.gov/pubmed/16547208'
}

class Base(object):
	'''
	This is the base class for the Warren/Heart AO Root.
		The form of these equations is:
		    y = mx + b
		    where x is log(bsa)
		    MSE is used for the 'sd'
		    
	'''

	def __init__(self, data, pt, limit ):
		self.source = name
		self.citation = citation
		self.siteName = data['name']
		self.refName = 'warren_heart_2006'
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
		return math.exp( self._mean(self.bsa) )

	def zscore(self):
		try:
			return (math.log(self.score) - self._mean(self.bsa)) / self.mse
		except:
			return None  # property of object 'pt' does not exist
	
	def uln(self):
		return math.exp( self._mean(self.bsa) + self.limit * self.mse ) 
	
	
	def lln(self):
		return math.exp( self._mean(self.bsa) - self.limit * self.mse ) 

	def chart_uln(self):
		return ( [[x, math.exp( self.limit * self.mse + self._mean(x) )] for x in self.bsaData] )
	def chart_lln(self):
		return ( [[x, math.exp( -self.limit * self.mse + self._mean(x) )] for x in self.bsaData] )

# 
# individual site data 
#

aov = { 'name': 'aov', 'slope': 0.426, 'intercept': 2.732, 'mse': 0.10392 }
sov = { 'name': 'sov', 'slope': 0.443, 'intercept': 3.021, 'mse': 0.10173 }
stj = { 'name': 'stj', 'slope': 0.434, 'intercept': 2.819, 'mse': 0.10961 }
aao = { 'name': 'aao', 'slope': 0.421, 'intercept': 2.898, 'mse': 0.09111 }


sites = [
    'aov',
    'sov',
    'stj',
    'aao'
    ]

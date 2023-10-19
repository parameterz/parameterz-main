#!/usr/bin/env python

from __future__ import division
import math

required = ['bsa', 'gender']
bsaMethod = 'Dubois'
constraints = {'age': [0, 18], 'bsa': [0, 2.0]}

name = 'Zilberman et al., Ped. Card. 2005'
description = 'Gender and BSA-adjusted z-scores for the cardiac valves; Cincinnati data.'
detail = '''Determine BSA-adjusted z-scores for the mitral valve, aortic valve,
tricuspid valve, and pulmonic valve using this calculator.
The regression equations are those from Cincinnati Children's Hospital,
based on over 700 children between the ages of 0-18 years.
'''
critique = {
  'model': 'log-log with BSA',
  'subjects': 748,
  'heterosc': False,
  'residual_assoc': False,
  'residual_heterosc': False,
  'distribution': False
}

year = '2005'
citation = {
	'title': '''Two-dimensional echocardiographic valve measurements in
	healthy children: gender-specific differences.''',
	'authors': 'Zilberman MV, Khoury PR, Kimball RT.',
	'journal': 'Pediatr Cardiol. 2005 Jul-Aug;26(4):356-60.',
	'url': 'http://www.ncbi.nlm.nih.gov/pubmed/16374684'
}

class Base(object):
	'''
	This is the base class for the Zilberman/Cincinnati valve data.
		The form of these equations is a log-log transformation:
		    log(y) = m*log(x) + b
		    where x is bsa
		    MSE is used for the 'sd'
		    
	'''

	def __init__(self, data, pt, limit ):
		self.source = name
		self.citation = citation
		self.siteName = data['name']
		self.refName = 'zilberman_pedcard_2005'
		self.data = data['girls'] if pt.gender == 'f' else data['boys']
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
		return self.data['slope'] * math.log( bsa ) + self.data['intercept']
		
	def mean(self):
		return math.exp( self._mean(self.bsa) ) * 10
	
	def zscore(self):
		try:
		    return ( math.log( self.score / 10 ) - self._mean(self.bsa) ) / self.data['mse']
		except:
		    return None #property of object 'pt' does not exist
		
	def uln(self):
		return math.exp( self._mean(self.bsa) + self.limit * self.data['mse'] ) * 10
	
	def lln(self):
		return math.exp( self._mean(self.bsa) - self.limit * self.data['mse'] ) * 10
	
	def chart_uln(self):
		return ( [[x, 10 * math.exp( self.limit * self.data['mse'] + self._mean(x) )] for x in self.bsaData] )
	def chart_lln(self):
		return ( [[x, 10 * math.exp( -self.limit * self.data['mse'] + self._mean(x) )] for x in self.bsaData] )

# 
# individual site data 
#

aov = { 'name': 'aov',
	'boys': {'slope': 0.492, 'intercept': 0.472, 'mse': 0.141 },
	'girls': {'slope': 0.461, 'intercept': 0.437, 'mse': 0.127 }
}
pv = { 'name': 'pv',
	'boys': {'slope': 0.498, 'intercept': 0.618, 'mse': 0.152 },
	'girls': {'slope': 0.476, 'intercept': 0.597, 'mse': 0.144 }
}
mvd_l = { 'name': 'mvd_l',
	'boys': {'slope': 0.425, 'intercept': 0.765, 'mse': 0.169 },
	'girls': {'slope': 0.408, 'intercept': 0.733, 'mse': 0.180 }
}
tvd_l = { 'name': 'tvd_l',
	'boys': {'slope': 0.391, 'intercept': 0.817, 'mse': 0.171 },
	'girls': {'slope': 0.364, 'intercept': 0.755, 'mse': 0.186 }
}

sites = [
    'aov',
    'pv',
    'mvd_l',
    'tvd_l'
    ]


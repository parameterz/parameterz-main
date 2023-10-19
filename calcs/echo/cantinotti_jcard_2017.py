#!/usr/bin/env python

from __future__ import division
import math

required = ['bsa']
bsaMethod = 'Haycock'
constraints = {'age': [0, 17], 'bsa': [0.12, 2.12]}

name = 'Cantinotti et al., J Cardiol 2017'
description = 'BSA-adjusted z-scores for valve and arterial dimensions.'
detail = '''Calculate BSA-adjusted z-scores of common valvular and arterial dimensions, such as the aortic
and mitral valves, aorta and aortic arch, and pulmonary arteries.
>The primary aim of this investigation was to establish pediatric
nomograms for two-dimensional (2D) echocardiographic valvular
and arterial measurements derived from a wide population of
healthy neonates, infants and children.
'''
critique = {
  'model': 'log-log with BSA',
  'subjects': 1151,
  'heterosc': True,
  'residual_assoc': False,
  'residual_heterosc': False,
  'distribution': True,
  'source': 'parameterz'
}

year = '2017'
citation = {
	'title': 'Nomograms for two-dimensional echocardiography derived valvular and arterial dimensions in Caucasian children.',
	'authors': 'Cantinotti M, Giordano R, Scalese M, Murzi B, Assanta N, Spadoni I, Maura C, Marco M, Molinaro S, Kutty S, Iervasi G.',
	'journal': 'J Cardiol. 2017 Jan;69(1):208-215.',
	'url': 'http://www.ncbi.nlm.nih.gov/pubmed/27118699'
}

class Base(object):
	'''
	This is the base class for the Cantinotti 2017 data.
		The form of these equations is:
		    ln(y) = m*ln(x) + b
		    where x is bsa
		    MSE is used for the 'sd'
		    
	'''

	def __init__(self, data, pt, limit ):
		self.source = name
		self.citation = citation
		self.siteName = data['name']
		self.refName = 'cantinotti_jcard_2017'
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
		    return ( math.log( self.score ) - self._mean(self.bsa) ) / self.mse
		except:
		    return None #property of object 'pt' does not exist
	
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

tvd_l = { 'name': 'tvd_l', 'intercept': 3.187, 'slope': 0.466, 'mse': 0.140 }
mvd_l = { 'name': 'mvd_l', 'intercept': 3.161, 'slope': 0.471, 'mse': 0.087 }
aov = { 'name': 'aov', 'intercept': 2.750, 'slope': 0.515, 'mse': 0.088 }
sov = { 'name': 'sov', 'intercept': 3.051, 'slope': 0.481, 'mse': 0.092 }
stj = { 'name': 'stj', 'intercept': 2.797, 'slope': 0.512, 'mse': 0.098 }
aao = { 'name': 'aao', 'intercept': 2.949, 'slope': 0.486, 'mse': 0.096 }
prox_arch = { 'name': 'prox_arch', 'intercept': 2.742, 'slope': 0.515, 'mse': 0.121 }
dist_arch = { 'name': 'dist_arch', 'intercept': 2.572, 'slope': 0.521, 'mse': 0.124 }
isthmus = { 'name': 'isthmus', 'intercept': 2.356, 'slope': 0.550, 'mse': 0.146 }
dao = { 'name': 'dao', 'intercept': 2.518, 'slope': 0.498, 'mse': 0.130 }
abd_ao = { 'name': 'abd_ao', 'intercept': 2.352, 'slope': 0.477, 'mse': 0.122 }
ivc = { 'name': 'ivc', 'intercept': 2.406, 'slope': 0.826, 'mse': 0.240 }
pv = { 'name': 'pv', 'intercept': 2.908, 'slope': 0.538, 'mse': 0.113 }
mpa = { 'name': 'mpa', 'intercept': 2.945, 'slope': 0.489, 'mse': 0.112 }
lpa = { 'name': 'lpa', 'intercept': 2.383, 'slope': 0.569, 'mse': 0.159 }
rpa = { 'name': 'rpa', 'intercept': 2.397, 'slope': 0.558, 'mse': 0.145 }


sites = [
	'tvd_l',
	'mvd_l',
    'aov',
    'sov',
    'stj',
    'aao',
	'prox_arch',
	'dist_arch',
	'isthmus',
	'dao',
	'abd_ao',
	'ivc',
	'pv',
	'mpa',
	'rpa',
	'lpa'
    ]


#!/usr/bin/env python

from __future__ import division
import math

required = ['bsa']
bsaMethod = 'Haycock'
constraints = {'age': [0, 18]}

name = 'McCrindle et al., Circ 2007'
description = 'BSA-adjusted z-scores for the proximal coronary arteries.'
detail = '''Z-scores normalized to BSA for the left main coronary artery (LMCA),
left anterior descending (LAD), and right main coronary artery (RCA). Data from
Boston Children's Hospital.
'''
critique = {
  'model': 'nonlinear/allometric model with BSA',
  'subjects': 221,
  'heterosc': False,
  'residual_assoc': False,
  'residual_heterosc': False,
  'distribution': False,
  'source': 'parameterz'
}
year = '2007'
citation = {
	'title': '''Coronary artery involvement in children with Kawasaki
	disease: risk factors from analysis of serial
	normalized measurements.''',
	'authors': '''McCrindle BW, Li JS, Minich LL, Colan SD, Atz AM,
	Takahashi M, Vetter VL, Gersony WM, Mitchell PD,
	Newburger JW; Pediatric Heart Network Investigators.''',
	'journal': 'Circulation. 2007 Jul 10;116(2):174-9.',
	'url': 'http://www.ncbi.nlm.nih.gov/pubmed/17576863'
}

class Base(object):
	'''
	This is the base class for the Boston coronary arteries.
		The form of these equations is:
		    y = m*x^c + b
		    where x = BSA (raised to an exponenent, c)
		    
	'''

	def __init__(self, data, pt, limit ):
		self.source = name
		self.citation = citation
		self.siteName = data['name']
		self.refName = 'mccrindle_circ_2007'
		self.a1 = data['a1']
		self.b1 = data['b1']
		self.a2 = data['a2']
		self.b2 = data['b2']
		self.exp = data['exp']
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
		#convert cm:mm
		return 10 * (self.a1 + self.b1 * math.pow(bsa, self.exp))
	def mean(self):
		return  self._mean(self.bsa)
	
	def sd(self, bsa):
		return 10 * (self.a2 + self.b2 * bsa)
	
	def zscore(self):
		try:
		    return (self.score - self.mean()) / self.sd(self.bsa) 
		except:
		    return None #property of object 'pt' does not exist
	
	def uln(self):
		return self.mean() + self.limit * self.sd(self.bsa) 
	
	def lln(self):
		return self.mean() - self.limit * self.sd(self.bsa) 

	def chart_uln(self):
		return ( [[x, ( self.limit * self.sd(x) + self._mean(x) )] for x in self.bsaData] )
	def chart_lln(self):
		return ( [[x, ( -self.limit * self.sd(x) + self._mean(x) )] for x in self.bsaData] )



# 
# individual site data 
#

lmca = { 'name': 'lmca', 'a1': -0.02887, 'b1': 0.31747, 'exp': 0.36008, 'a2': 0.03040, 'b2': 0.01514 }
lad = { 'name': 'lad', 'a1': -0.02852, 'b1': 0.26108, 'exp': 0.37893, 'a2': 0.01465, 'b2': 0.01996 }
prox_rca = { 'name': 'prox_rca', 'a1': -0.02756, 'b1': 0.26117, 'exp': 0.39992, 'a2': 0.02407, 'b2': 0.01597 }

sites = [
    'lmca',
    'lad',
    'prox_rca'
    ]


#!/usr/bin/env python

from __future__ import division
import math

required = ['bsa']
bsaMethod = 'Dubois'
constraints = {'bsa': [0, 2.0], 'age': [0 ,18]}

name = 'Pettersen et al., JASE 2008'
description = 'BSA-adjusted z-scores for cardiac structures; Detroit data'
detail = '''BSA-adjusted z-scores of 21 common 2D and M-Mode echo measurements.
Measurement sites include the mitral valve, left ventricle, aortic valve,
aortic arch, pulmonary valve, and pulmonary arteries.
Data is from 782 patients evaluated at the Children's Hospital of Michigan.
'''

critique = {
  'model': 'Third-order polynomial with log-transformed dependent variable (BSA)',
  'subjects': 782,
  'heterosc': 'unk',
  'residual_assoc': False,
  'residual_heterosc': False,
  'distribution': False
}
year = '2008'
citation = {
	'title': '''Regression equations for calculation of z scores of cardiac
	structures in a large cohort of healthy infants, children, and
	adolescents: an echocardiographic study.''',
	'authors': 'Pettersen MD, Du W, Skeens ME, Humes RA.',
	'journal': 'J Am Soc Echocardiogr. 2008 Aug;21(8):922-34.',
	'url': 'http://www.ncbi.nlm.nih.gov/pubmed/18406572'
}

class Base(object):
	'''
	This is the base class for the Detroit data.
	The form of these equations is a third-order polynomial:
	    y = 'intercept' + (b1 * bsa) + (b2 * Math.pow(bsa, 2)) + (b3 * Math.pow(bsa, 3))
	    and 'sd' = Math.sqrt(data.mse)

	'''

	def __init__(self, data, pt, limit ):
		self.source = name
		self.citation = citation
		self.siteName = data['name']
		self.refName = 'pettersen_jase_2008'
		self.intercept = data['intercept']
		self.b1 = data['b1']
		self.b2 = data['b2']
		self.b3 = data['b3']
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
		return self.intercept + (self.b1 * bsa) + (self.b2 * math.pow(bsa, 2)) + (self.b3 * math.pow(bsa, 3))
		
	def mean(self):
		return 10 * math.exp( self._mean(self.bsa) )
	
	def sd(self):
		return math.sqrt(self.mse)
	
	def zscore(self):
		try:
		    return (math.log(self.score/10) - self._mean(self.bsa)) / self.sd() #convert score to 'cm'
		except:
		    return None #property of object 'pt' does not exist
	
	def uln(self):
		return math.exp( self._mean(self.bsa) + self.limit * self.sd() ) * 10
	
	
	def lln(self):
		return math.exp( self._mean(self.bsa) - self.limit * self.sd() ) * 10

	def chart_uln(self):
		return ( [[x, 10 * math.exp( self.limit * self.sd() + self._mean(x) )] for x in self.bsaData] )
	def chart_lln(self):
		return ( [[x, 10 * math.exp( -self.limit * self.sd() + self._mean(x) )] for x in self.bsaData] )




# 
# individual site data 
#
rvd_mm = { 'name': 'rvd_mm', 'intercept': -0.317, 'b1': 1.85, 'b2': -1.274, 'b3': 0.335, 'mse': 0.058 }
ivsd_mm = { 'name': 'ivsd_mm', 'intercept': -1.242, 'b1': 1.272, 'b2': -0.762, 'b3': 0.208, 'mse': 0.046 }
ivss_mm = { 'name': 'ivss_mm', 'intercept': -1.048, 'b1': 1.751, 'b2': -1.177, 'b3': 0.318, 'mse': 0.034 }
lvedd_mm = { 'name': 'lvedd_mm', 'intercept': 0.105, 'b1': 2.859, 'b2': -2.119, 'b3': 0.552, 'mse': 0.01 }
lvesd_mm = { 'name': 'lvesd_mm', 'intercept': -0.371, 'b1': 2.833, 'b2': -2.081, 'b3': 0.538, 'mse': 0.016 }
lvpwd_mm = { 'name': 'lvpwd_mm', 'intercept': -1.586, 'b1': 1.849, 'b2': -1.188, 'b3': 0.313, 'mse': 0.037 }
lvpws_mm = { 'name': 'lvpws_mm', 'intercept': -0.947, 'b1': 1.907, 'b2': -1.259, 'b3': 0.33, 'mse': 0.023 }
aov = { 'name': 'aov', 'intercept': -0.874, 'b1': 2.708, 'b2': -1.841, 'b3': 0.452, 'mse': 0.01 }
sov = { 'name': 'sov', 'intercept': -0.5, 'b1': 2.537, 'b2': -1.707, 'b3': 0.42, 'mse': 0.012 }
stj = { 'name': 'stj',  'intercept': -0.759, 'b1': 2.643, 'b2': -1.797, 'b3': 0.442, 'mse': 0.018 } 
prox_arch = { 'name': 'prox_arch', 'intercept': -0.79, 'b1': 3.02, 'b2': -2.484, 'b3': 0.712, 'mse': 0.023 } 
isthmus = { 'name': 'isthmus', 'intercept': -1.072, 'b1': 2.539, 'b2': -1.627, 'b3': 0.368, 'mse': 0.027 }
dao = { 'name': 'dao', 'intercept': -0.976, 'b1': 2.469, 'b2': -1.746, 'b3': 0.445, 'mse': 0.026 }
abd_ao = { 'name': 'abd_ao', 'intercept': -0.922, 'b1': 2.1, 'b2': -1.411, 'b3': 0.371, 'mse': 0.018 } 
pv = { 'name': 'pv', 'intercept': -0.761, 'b1': 2.774, 'b2': -1.808, 'b3': 0.436, 'mse': 0.023 } 
mpa = { 'name': 'mpa', 'intercept': -0.707, 'b1': 2.746, 'b2': -1.807, 'b3': 0.424, 'mse': 0.024 } 
rpa = { 'name': 'rpa', 'intercept': -1.36, 'b1': 3.394, 'b2': -2.508, 'b3': 0.66, 'mse': 0.027 } 
lpa = { 'name': 'lpa', 'intercept': -1.348, 'b1': 2.884, 'b2': -1.954, 'b3': 0.466, 'mse': 0.028 } 
mvd_l = { 'name': 'mvd_l', 'intercept': -0.271, 'b1': 2.446, 'b2': -1.7, 'b3': 0.425, 'mse': 0.022 } 
tvd_l = { 'name': 'tvd_l', 'intercept': -0.164, 'b1': 2.341, 'b2': -1.596, 'b3': 0.387, 'mse': 0.036 } 
la = { 'name': 'la', 'intercept': -0.208, 'b1': 2.164, 'b2': -1.597, 'b3': 0.429, 'mse': 0.02} 

sites = [
    'aov', 'sov', 'stj', 'prox_arch', 'isthmus', 'dao', 'abd_ao', 'pv', 'mpa', 'rpa', 'lpa', 'la',
    'mvd_l', 'tvd_l', 'lad_2d', 'rvd_mm', 'ivsd_mm', 'lvedd_mm', 'lvpwd_mm', 'ivss_mm', 'lvesd_mm',
    'lvpws_mm'
    ]


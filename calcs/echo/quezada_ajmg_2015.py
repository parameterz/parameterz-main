#!/usr/bin/env python

from __future__ import division
import math

required = ['bsa']
bsaMethod = 'Haycock'
constraints = {'bsa': [0.4, 2.75], 'age': [3, 70]}

omitFromSites = True  #too confusing to include this in with the others since it is speci

name = 'Quezada et al., Am J Med Gen 2015'
description = 'BSA-adjusted z-scores for the aortic root in girls and women with Turner syndrome'
detail = '''BSA-adjusted z-scores for the aortic valve, aortic root, and aortic arch &mdash; developed _specifically for Turner syndrome patients_.
>The information presented here should decrease the bias introduced
>by making comparisons with a taller and larger non-Turner reference
>population. 
'''

critique = {
  'model': 'Third-order polynomial with log-transformed dependent variable (BSA)',
  'subjects': 481,
  'heterosc': 'unk',
  'residual_assoc': False,
  'residual_heterosc': False,
  'distribution': False
}
year = '2015'
citation = {
	'title': 'Aortic dimensions in Turner syndrome.',
	'authors': 'Quezada E, Lapidus J, Shaughnessy R, Chen Z, Silberbach M.',
	'journal': 'Am J Med Genet A. 2015 Nov;167A(11):2527-32.',
	'url': 'http://www.ncbi.nlm.nih.gov/pubmed/26118429'
}

class Base(object):
	'''
	This is the base class for the Quezada data, loosely based on the Detroit model
	The form of these equations is a second-order polynomial:
	    y = 'intercept' + (b1 * bsa) + (b2 * Math.pow(bsa, 2)) 
	    and 'sd' = Math.sqrt(mse). Main difference with the Detroit data is that these use a square root, not log, transformation.

	'''

	def __init__(self, data, pt, limit ):
		self.source = name
		self.citation = citation
		self.siteName = data['name']
		self.refName = 'quezada_ajmg_2015'
		self.intercept = data['intercept']
		self.b1 = data['b1']
		self.b2 = data['b2']
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
		return self.intercept + (self.b1 * bsa) + (self.b2 * math.pow(bsa, 2)) 
		
	def mean(self):
		return 10 * math.pow( self._mean(self.bsa), 2 )
	
	def sd(self):
		return math.sqrt(self.mse)
	
	def zscore(self):
		try:
		    return (math.sqrt(self.score/10) - self._mean(self.bsa)) / self.sd() #convert score to 'cm'
		except:
		    return None #property of object 'pt' does not exist
	
	def uln(self):
		return math.pow( ( self._mean( self.bsa ) + self.limit * self.sd() ) , 2 ) * 10
	
	
	def lln(self):
		return math.pow( ( self._mean( self.bsa ) - self.limit * self.sd() ) , 2 ) * 10

	def chart_uln(self):
		return ( [[x, 10 * math.pow( self.limit * self.sd() + self._mean(x), 2 )] for x in self.bsaData] )
	def chart_lln(self):
		return ( [[x, 10 * math.pow( -self.limit * self.sd() + self._mean(x), 2 )] for x in self.bsaData] )




# 
# individual site data 
#
aov = { 'name': 'aov', 'intercept': 0.891, 'b1': 0.414, 'b2': -0.081, 'mse': 0.007 }
sov = { 'name': 'sov', 'intercept': 1.035, 'b1': 0.589, 'b2': -0.129, 'mse': 0.009 }
stj = { 'name': 'stj',  'intercept': 0.895, 'b1': 0.586, 'b2': -0.124, 'mse': 0.009 }
aao = { 'name': 'aao', 'intercept': 0.942, 'b1': 0.593, 'b2': -0.122, 'mse': 0.012  }
prox_arch = { 'name': 'prox_arch', 'intercept': 0.881, 'b1': 0.539, 'b2': -0.107, 'mse': 0.012 }
dist_arch = { 'name': 'dist_arch', 'intercept': 0.844, 'b1': 0.428, 'b2': -0.072, 'mse': 0.012 }
isthmus = { 'name': 'isthmus', 'intercept': 0.895, 'b1': 0.279, 'b2': -0.038, 'mse': 0.014 }
dao = { 'name': 'dao', 'intercept': 0.676, 'b1': 0.503, 'b2': -0.094, 'mse': 0.009 }

sites = [
    'aov', 'sov', 'stj', 'aao', 'prox_arch', 'dist_arch', 'isthmus', 'dao'
    ]


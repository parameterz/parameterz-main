#!/usr/bin/env python

from __future__ import division
import math

required = ['wt']

constraints = {'age': [1, 17], 'weight': [8.2, 91.4]}

name = 'Neilan et al., Eur J Echocardiogr 2009'
description = 'weight-adjusted z-scores for left atrial diameter.'
detail = '''Allometric scaling model developed by  investigators at Mass. General Hospital
on over 4,000 patients.(!)
>Conventional linear correction for body size is inaccurate in children and
>paradoxically increases the relationship of the indexed parameter with
>WT and BSA. Conversely, correction using the optimal AE removes the effect of that variable
'''
critique = {
  'model': 'Log-log model with BSA or weight',
  'subjects': 4109,
  'heterosc': True,
  'residual_assoc': True,
  'residual_heterosc': True,
  'distribution': False
}  
year = '2009'
citation = {
	'title': 'Derivation of a size-independent variable for scaling of cardiac dimensions in a normal paediatric population.',
	'authors': 'Neilan TG, Pradhan AD, King ME, Weyman AE.',
	'journal': 'Eur J Echocardiogr. 2009 Jan;10(1):50-5.',
	'url': 'http://www.ncbi.nlm.nih.gov/pubmed/18490317'
}

class Base(object):
	'''
	This is the base class for the Neilan LA diameter calculations,
	indexing to a size-independent value using an allometric relationship on weight
		
	'''

	def __init__(self, data, pt, limit ):
		self.source = name
		self.citation = citation
		self.siteName = data['name']
		self.refName = 'neilan_eje_2009'
		self.limit = limit
		self.score = float(getattr(pt, data['name']))
		self.wt = float(pt.wt)
		#chart stuff
		self.chartData = True
		self.chartXAxisLabel = 'Weight'
		self.myData = ( [[self.wt, self.score]] )#plot data
		self.constraints = constraints
		self.critique = critique

	def mean(self):
			return 10.665 * math.pow( self.wt, 0.252 )
		
	
	def zscore(self):
		#transform LA diam into 'indexed' value
		score = ( self.score  ) / (10.665 * math.pow( self.wt, 0.252 ))
		mean = 1.008
		sd = 0.121
		return ( score - mean ) / sd

	def lln(self):
		return  ( 1.008 - 0.121 * self.limit ) * 10.665 * math.pow( self.wt, 0.252 )

	def uln(self):
		return  ( 1.008 + 0.121 * self.limit ) * 10.665 * math.pow( self.wt, 0.252 )

	def chart_lln(self):
		#chart range s/b 0.1 - 100 kg
		bsaRange = [x * 0.1 for x in range(10, 1000)]
		return ( [[x, 10 * ( 1.008 - 0.121 * self.limit ) * math.pow( x, 0.252 )] for x in bsaRange] )

	def chart_uln(self):
		#chart range s/b 0.1 - 100 kg
		bsaRange = [x * 0.1 for x in range(10, 1000)]
		return ( [[x, 10 * ( 1.008 + 0.121 * self.limit ) * math.pow( x, 0.252 )] for x in bsaRange] )


# 
# individual site data 
#

la = { 'name': 'la'} 


sites = [
    'la'
    ]

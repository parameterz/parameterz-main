#!/usr/bin/env python

from __future__ import division
import math

required = ['bsa']
bsaMethod = 'Haycock'
constraints = {'age': [0, 18], 'bsa': [0.17, 2.3]}

name = 'Bhatla et al., Circ Cardiovasc Imaging 2012'
year = '2012'
description = 'BSA-adjusted z-scores for left atrial volume.'

detail = '''BSA-adjusted z-scores of left atrial volume, measured using the
biplane area length method. Volumes are adjusted for body size using allometric
equations (allometric exponents are different for children on either side of 1m<sup>2</sup>).
'''

critique = {
  'model': 'Indexed to BSA<sup>1.48</sup> or to BSA<sup>1.08</sup> (allometric model)',
  'subjects': 300,
  'heterosc': True,
  'residual_assoc': True,
  'residual_heterosc': True,
  'distribution': True,
  'source': 'parameterz'
}

citation = {
	'title': 'Normal Values of Left Atrial Volume in Pediatric Age Group Using a Validated Allometric Model.',
	'authors': 'Bhatla P, Nielsen JC, Ko HH, Doucette J, Lytrivi ID, Srivastava S.',
	'journal': 'Circ Cardiovasc Imaging. 2012 Oct 16.',
	'url': 'http://www.ncbi.nlm.nih.gov/pubmed/23074344'
}

class Base(object):
	'''
	This is the base class for the Bhatla LA Volume calculations.
		
	'''

	def __init__(self, data, pt, limit ):
		self.source = name
		self.citation = citation
		self.siteName = data['name']
		self.refName = 'bhatla_circimaging_2012'
		self.limit = limit
		self.bsaMethod = bsaMethod
		self.bsa = pt.bsa(bsaMethod)
		self.score = float(getattr(pt, data['name']))
		#chart stuff
		self.chartData = True
		self.chartXAxisLabel = 'BSA'
		self.myData = ( [[self.bsa, self.score]] )#plot data
		self.constraints = constraints
		self.critique = critique

	def mean(self):
		if self.bsa <= 1:
			# ae = 1.48
			return 31.5 * math.pow( self.bsa, 1.48 )
		else:
			#ae = 1.08
			return 26 * math.pow( self.bsa, 1.08 )
		
	
	def zscore(self):
		if self.bsa <= 1:
			#transform LA vol into 'indexed' value
			# ae = 1.48
			score = self.score / math.pow( self.bsa, 1.48 )
			mean = 31.5
			sd = 5.5
			return ( score - mean ) / sd
		else:
			#transform LA vol into 'indexed' value
			#ae = 1.08
			score = self.score / math.pow( self.bsa, 1.08 )
			mean = 26
			sd = 4.2
			return ( score - mean ) / sd

	def lln(self):
		if self.bsa <= 1:
			# ae = 1.48
			return ( 31.5 - 5.5 * self.limit ) * math.pow( self.bsa, 1.48 )
		else:
			#ae = 1.08
			return ( 26 - 4.2 * self.limit ) * math.pow( self.bsa, 1.08 )

	def uln(self):
		if self.bsa <= 1:
			# ae = 1.48
			return ( 31.5 + 5.5 * self.limit ) * math.pow( self.bsa, 1.48 )
		else:
			#ae = 1.08
			return ( 26 + 4.2 * self.limit ) * math.pow( self.bsa, 1.08 )

	def chart_lln(self):
		if self.bsa <= 1:
			# chart range s/b 0.1 - 1.0 m^2
			bsaRange = [x * 0.1 for x in range(1, 11)]
			# ae = 1.48
			return ( [[x, ( 31.5 - 5.5 * self.limit ) * math.pow( x, 1.48 )] for x in bsaRange] )

		else:
			#chart range s/b 1.1 - 2.1 m^2
			bsaRange = [x * 0.1 for x in range(10, 22)]
			#ae = 1.08
			return ( [[x, ( 26 - 4.2 * self.limit ) * math.pow( x, 1.08 )] for x in bsaRange] )

	def chart_uln(self):
		if self.bsa <= 1:
			# chart range s/b 0.1 - 1.0 m^2
			bsaRange = [x * 0.1 for x in range(1, 11)]
			# ae = 1.48
			return ( [[x, ( 31.5 + 5.5 * self.limit ) * math.pow( x, 1.48 )] for x in bsaRange] )

		else:
			#chart range s/b 1.1 - 2.1 m^2
			bsaRange = [x * 0.1 for x in range(10, 22)]
			#ae = 1.08
			return ( [[x, ( 26 + 4.2 * self.limit ) * math.pow( x, 1.08 )] for x in bsaRange] )


# 
# individual site data 
#

lav = { 'name': 'lav'} 


sites = [
    'lav'
    ]

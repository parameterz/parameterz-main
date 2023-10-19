#!/usr/bin/env python

from __future__ import division
import math
import logging

required = ['bsa']
constraints = {'age': [0, 3], 'bsa': [0.21, 0.66]}
bsaMethod = 'Haycock' 
name = 'Lytrivi et al., JASE 2011'
description = 'BSA-adjusted z-scores for left ventricular end-diastolic volume.'
detail = '''BSA-adjusted Z-scores for LVEDV by the subxiphoid bullet technique using an allometeric model.
Data from 100 patients &le; 3 years from researchers at Mount Sinai
School of Medicine, New York, New York.
Post-hoc testing demonstrated a normal distribution of z-scores.
'''
critique = {
  'model': 'Indexed to BSA<sup>1.38</sup> (allometric model)',
  'subjects': 100,
  'heterosc': False,
  'residual_assoc': True,
  'residual_heterosc': False,
  'distribution': True
}

year = '2011'
citation = {
	'title': 'Normal values for left ventricular volume in infants and young children by the echocardiographic subxiphoid five-sixth area by length (bullet) method.',
	'authors': 'Lytrivi ID, Bhatla P, Ko HH, Yau J, Geiger MK, Walsh R, Parness IA, Srivastava S, Nielsen JC.',
	'journal': 'J Am Soc Echocardiogr. 2011 Feb;24(2):214-8.',
	'url': 'http://www.ncbi.nlm.nih.gov/pubmed/21281912'
}

class Base(object):
	'''
	This is the base class for the Lytrivi LVEDV calculations.
		
	'''

	def __init__(self, data, pt, limit ):
		self.source = name
		self.citation = citation
		self.siteName = data['name']
		self.refName = 'lytrivi_jase_2011'
		self.limit = limit
		self.bsaMethod = bsaMethod
		self.bsa = pt.bsa(bsaMethod)
		self.bsa_i = math.pow(self.bsa, 1.38)
		self.score = float(getattr(pt, data['name']))
		#chart stuff
		self.chartData = True
		self.bsaData = [x * 0.1 for x in range(1, 21)]
		self.chartXAxisLabel = 'BSA'
		self.myData = ( [[self.bsa, self.score]] )#plot data
		self.constraints = constraints
		self.critique = critique

	def mean(self):
		return 70.4 * self.bsa_i 
	
	def zscore(self):
		try:
			return ( self.score / self.bsa_i  - 70.4 ) / 9.1
		except:
		    return None #property of object 'pt' does not exist
		
	def uln(self):
		return (self.limit * 9.1 + 70.4) *  self.bsa_i
	
	def lln(self):
		return (-self.limit * 9.1 + 70.4) *  self.bsa_i
	
	def chart_uln(self):
		return ( [[x, (self.limit * 9.1 + 70.4) *  math.pow(x, 1.38) ] for x in self.bsaData] )
			
	def chart_lln(self):
		return ( [[x, (-self.limit * 9.1 + 70.4) *  math.pow(x, 1.38) ] for x in self.bsaData] )


# 
# individual site data 
#

lvedv = { 'name': 'lvedv' } 

sites = [
	'lvedv',
]

#!/usr/bin/env python

from __future__ import division
import math
import logging

required = ['bsa']
bsaMethod = 'Haycock' #not published in text of article!?!
constraints = {'age': [6, 62], 'bsa': [0.5, 2.5]}

name = 'Gentles et al., JACC Cardiovasc Imaging 2012'
description = 'BSA-adjusted z-scores for left ventricular volume and diameter.'
detail = '''BSA-adjusted z-scores of LV volumes and diameters. Data provided
as supplemental material to a discussion on ventricular dysfunction
following surgery for aortic regurgitation.
>Failure to correct ESV for body size introduces systematic bias to risk assessment.
'''
critique = {
  'model': 'log-log with BSA',
  'subjects': 158,
  'heterosc': False,
  'residual_assoc': False,
  'residual_heterosc': False,
  'distribution': False,
  'source': 'parameterz'
}
year = '2012'
citation = {
	'title': 'Normalized End-Systolic Volume and Preload Reserve Predict Ventricular Dysfunction Following Surgery for Aortic Regurgitation Independent of Body Size',
	'authors': 'Gentles TL, French JK, Zeng I, Milsom PF, Finucane AK, Wilson NJ.',
	'journal': 'JACC Cardiovasc Imaging. 2012 Jun;5(6):626-33.',
	'url': 'http://www.ncbi.nlm.nih.gov/pubmed/22698533'
}

class Base(object):
	'''
	This is the base class for the Gentles calculations.
		
	'''

	def __init__(self, data, pt, limit ):
		self.source = name
		self.citation = citation
		self.siteName = data['name']
		self.refName = 'gentles_jacc_2012'
		self.limit = limit
		self.bsaMethod = bsaMethod
		self.bsa = pt.bsa(bsaMethod)
		self.score = float(getattr(pt, data['name']))
		self.slope = data['slope']
		self.exp = data['exp']
		self.syx = data['syx']
		#chart stuff
		self.chartData = True
		self.bsaData = [x * 0.1 for x in range(1, 21)]
		self.chartXAxisLabel = 'BSA'
		self.myData = ( [[self.bsa, self.score]] )#plot data
		self.constraints = constraints
		self.critique = critique


	def _mean(self, bsa):
		return self.slope * math.pow(bsa, self.exp)
		
	def mean(self):
		mean = self.slope * math.pow(self.bsa, self.exp)
		if self.siteName == 'lvedd_mm' or self.siteName == 'lvesd_mm':
			#need to adjust units from cm to mm
			mean *= 10
		return mean

	def sd(self, bsa):
		meanX = 0.4594
		lxx = 12.294
		num = 158
		sd = math.log(bsa) - meanX
		#logging.info('step1: %s' %sd)
		sd = math.pow(sd, 2)
		#logging.info('step2: %s' %sd)
		sd /= lxx
		#logging.info('step3: %s' %sd)
		sd += 1/num
		#logging.info('step4: %s' %sd)
		sd += 1
		#logging.info('step5: %s' %sd)
		sd = math.pow(sd, 0.5)
		#logging.info('step6: %s' %sd)
		sd *= self.syx
		#logging.info('final step: %s' %sd)
		return sd
	
	def zscore(self):
		try:
			if self.siteName == 'lvedd_mm' or self.siteName == 'lvesd_mm': #need to adjust units from mm to cm
				return ( math.log( self.score/10 ) - math.log(self._mean(self.bsa)) ) / self.sd(self.bsa)
			else:
				return ( math.log( self.score ) - math.log(self._mean(self.bsa)) ) / self.sd(self.bsa)
		except:
		    return None #property of object 'pt' does not exist
		
	def uln(self):
		uln = math.exp( math.log(self._mean(self.bsa)) + self.limit * self.sd(self.bsa) )
		if self.siteName == 'lvedd_mm' or self.siteName == 'lvesd_mm':
			#need to adjust units from cm to mm
			uln *= 10
		return uln
	
	def lln(self):
		lln = math.exp( math.log(self._mean(self.bsa)) - self.limit * self.sd(self.bsa) )
		if self.siteName == 'lvedd_mm' or self.siteName == 'lvesd_mm':
			#need to adjust units from cm to mm
			lln *= 10
		return lln
	
	def chart_uln(self):
		if self.siteName == 'lvedd_mm' or self.siteName == 'lvesd_mm':
			return ( [[x, 10 * math.exp( math.log( self._mean(x)) + self.limit * self.sd(x) ) ] for x in self.bsaData] )
		else:
			return ( [[x, math.exp( math.log( self._mean(x)) + self.limit * self.sd(x) ) ] for x in self.bsaData] )
			
	def chart_lln(self):
		if self.siteName == 'lvedd_mm' or self.siteName == 'lvesd_mm':
			return ( [[x, 10 * math.exp( math.log( self._mean(x)) - self.limit * self.sd(x) ) ] for x in self.bsaData] )
		else:
			return ( [[x, math.exp( math.log( self._mean(x)) - self.limit * self.sd(x) ) ] for x in self.bsaData] )


# 
# individual site data 
#

lvedv = { 'name': 'lvedv', 'slope': 64.7, 'exp': 1.12, 'syx': 0.164 } 
lvesv = { 'name': 'lvesv', 'slope': 23.1, 'exp': 1.19, 'syx': 0.204 }
lvedd_mm = { 'name': 'lvedd_mm', 'slope': 3.88, 'exp': 0.40, 'syx': 0.071 }
lvesd_mm = { 'name': 'lvesd_mm', 'slope': 2.56, 'exp': 0.41, 'syx': 0.096 } # LVESD slope updated from "3.56" as is published to "2.56"- personal communication, T. Gentles 11/27/2012

sites = [
	'lvedv',
	'lvesv',
	'lvedd_mm',
	'lvesd_mm'
]

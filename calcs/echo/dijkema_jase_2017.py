#  !/usr/bin/env python

from __future__ import division
import math

required = ['wt']

constraints = {'age': [0, '6d'], 'wt': [0, '2kg']}
omitFromSites = True  # specific for premies

name = 'Dijkema et al., JASE 2017'
description = 'z-scores of the aortic arch for premature babies'

detail = '''Weight-adjusted z-scores of the aortic arch in premature babies (&le;2kg)

>The normative data can be used in diagnosis and decision making involving aortic arch pathology in premature infants.
'''

critique = {
    'model': 'nonlinear relationship with weight',
    'subjects': 385,
    'heterosc': False,
    'residual_assoc': False,
    'residual_heterosc': False,
    'distribution': True,
    'source': 'source article'
}
year = '2017'
citation = {
    'title': 'Normative Values of Aortic Arch Structures in Premature Infants.',
    'authors': 'Dijkema EJ, Molenschot MC, Breur JM, de Vries WB, Slieker MG.',
    'journal': 'J Am Soc Echocardiogr. 2017 Jan 27.',
    'url': 'http://www.ncbi.nlm.nih.gov/pubmed/28139441'
}


class Base(object):
    '''
    !!!UPDATE 7/26/2017!!!
    A correction was published in the July 2017 JASE that corrects the previously published and erroneous standard error
    data, so I am reverting back to the original type of calculations ...

    This is the base class for the Dijkema premie arch data.
    I had to change the design from regression-based to table/lookup based
    due to the fact that the prediction equation rarely predicted a mean that was consistent with
    either the table or chart; the suggest use of the 'standard error' in place of the sd for
     z-scoreing was way off. Published sd's from table data was usually around 0.6-0.8 mm; the published
     se's were 0.04-ish... way too small.
    '''

    def __init__(self, data, pt, limit):
        self.source = name
        self.citation = citation
        self.refName = 'dijkema_jase_2017'
        self.siteName = data['name']
        self.wt = float(pt.wt) * 1000 #convert kg to g
        self.limit = limit
        self.data = data
        self.score = float(getattr(pt, data['name']))
        # chart stuff
        self.chartData = False
        # self.bsaData = [x * 0.1 for x in range(1, 7)] #bsa range is 0.12-0.67
        # self.chartXAxisLabel = 'BSA'
        # self.myData = ( [[self.bsa, self.score]] )#plot data
        self.constraints = constraints
        self.critique = critique

    def mean(self):
        wt = self.wt
        int = self.data['intercept']
        b1 = self.data['b1']
        b2 = self.data['b2']
        b3 = self.data['b3']
        return int + ( b1 * wt ) + ( b2 * math.pow( wt, 2 ) ) + ( b3 * math.pow( wt, 3 ) )


    def sd(self):
        return self.data['se']


    def zscore(self):
        return ( self.score - self.mean() ) / self.sd()

    def uln(self):
        z = self.limit
        return self.mean() + z * self.sd()

    def lln(self):
        z = self.limit
        return self.mean() - z * self.sd()

    # def getIndex(self):
    #     wt = self.wt
    #     if wt < 1000:
    #         return 0
    #     if wt >= 1000 and wt < 1250:
    #         return 1
    #     if wt >= 1250 and wt < 1500:
    #         return 2
    #     if wt >= 1500 and wt < 1750:
    #         return 3
    #     else:
    #         return 4

aao = { "name": "aao", "intercept": 2.332, "b1": 0.004, "b2": -1.258e-6, "b3": 2.111e-10, "se": 0.62,
        "mean": [4.7, 5.2, 5.5, 5.7, 6.3],
        "sd": [0.6, 0.8, 0.6, 0.7, 0.7]
        }

dist_arch = { "name": "dist_arch", "intercept": 3.910, "b1": -0.001, "b2": 1.087e-6, "b3": -1.321e-10, "se": 0.61,
              "mean": [3.7, 3.9, 4.1, 4.3, 4.6],
              "sd": [0.6, 0.5, 0.5, 0.6, 0.8]
              }

isthmus = { "name": "isthmus", "intercept": 2.994, "b1": -0.001, "b2": 1.360e-6, "b3": -2.8381e-10, "se": 0.79,
            "mean": [2.8, 2.9, 3.1, 3.1, 3.6],
            "sd": [0.7, 0.7, 0.9, 0.8, 1.0]
            }
dao = { "name": "dao", "intercept": 4.131, "b1": -0.002, "b2": 2.799e-6, "b3": -7.4607e-10, "se": 0.78,
        "mean": [3.8, 3.8, 4.1, 4.3, 4.9],
        "sd": [0.6, 0.6, 0.8, 1.0, 1.2]
        }

sites = [

    'aao',
    'dist_arch',
    'isthmus',
    'dao'
]

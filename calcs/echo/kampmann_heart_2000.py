#!/usr/bin/env python

from __future__ import division
import math
import logging

required = ['bsa']
bsaMethod = 'Dubois'
constraints = {'age': [0, 18], 'bsa': [0, 2.0]}

name = 'Kampmann et al., Heart 2000'
description = 'BSA-adjusted z-scores for M-mode measurements in children.'
detail = '''BSA and weight-adjusted z-scores of M-mode measurements of the left
ventricle, right ventricle, and left atrial diameters (table data adapted to calculate z-scores).
>the presented charts and tables make it possible to judge
>echocardiographic measurements of a particular patient as normal or abnormal.
'''
critique = {
  'model': 'nonparametric; grouped by wt or BSA',
  'subjects': 2036,
  'heterosc': 'n/a',
  'residual_assoc': 'n/a',
  'residual_heterosc': 'n/a',
  'distribution': 'n/a',
  'source': 'parameterz'
}

year = '2000'
citation = {
    'title': '''Normal values of M mode echocardiographic measurements of
    more than 2000 healthy infants and children in central Europe.''',
    'authors': 'Kampmann C, Wiethoff CM, Wenzel A, Stolz G, Betancor M, Wippermann CF, Huth RG, Habermehl P, Knuf M, Emschermann T, Stopfkuchen H.',
    'journal': 'Heart. 2000 June; 83(6): 667-672.',
    'url': 'http://www.ncbi.nlm.nih.gov/pmc/articles/PMC1760862/'
}

class Base(object):
    '''
    This is the base class for the Kampmann M-Mode data.
    There are no equations; everything is a straight look-up,
    either by BSA or weight
            
    '''

    def __init__(self, data, pt, limit ):
        self.source = name
        self.citation = citation
        self.siteName = data['name']
        self.refName = 'kampmann_heart_2000'
        self.bsaData = data['bsaData']
        self.wtData = data['wtData']
        self.limit = limit
        self.bsaMethod = bsaMethod
        self.bsa = pt.bsa(bsaMethod)
        self.wt = float(pt.wt)
        self.score = float(getattr(pt, data['name']))
        self.use_bsa = (self.bsa >= 0.25)
        self.bsa_arr = [2, 1.75, 1.5, 1.4, 1.3, 1.2, 1.1, 1.0, 0.9, 0.8, 0.7, 0.65, 0.6, 0.55, 0.5, 0.45, 0.4, 0.35, 0.3, 0.275, 0.25]
        self.wt_arr = [4, 3.5, 3, 2.5, 2]
        #chart stuff
        self.chartData = True
        self.chartXAxisLabel = 'BSA' if self.use_bsa else 'Wt'
        self.myData = ( [[self.bsa if self.use_bsa else self.wt, self.score]] )#plot data
        self.constraints = constraints
        self.critique = critique


    def _getData(self):
        if self.use_bsa:
            arr = self.bsa_arr
            v = self.bsa
            data = self.bsaData
        else:
            if (self.wt >= 2):
                arr = self.wt_arr
                v = self.wt
                data = self.wtData
            else:
                logging.info('out of range: wt < cutoff')
                return None
            
        index = [ n for n,i in enumerate(arr) if v >= i ][0]
        return (data, index)
        
    def mean(self):
        data, index = self._getData()
        return data['mean'][index]
        
    def sd(self):
        if self.score >= self.mean():
            limit = 'upper'
        else:
            limit = 'lower'
        data, index = self._getData()
        return abs( (self.mean() - data[limit][index]) / 2 )
    
    def zscore(self):
        try:
            return ( self.score - self.mean() ) / self.sd()
        except:
            return None #property of object 'pt' does not exist
    
    def uln(self):
        data, index = self._getData()
        return data['upper'][index]
    
    def lln(self):
        data, index = self._getData()
        return data['lower'][index]

    def chart_uln(self):
        x = self.bsa_arr if self.use_bsa else self.wt_arr
        mean = self.bsaData['mean'] if self.use_bsa else self.wtData['mean']
        y = self.bsaData['upper'] if self.use_bsa else self.wtData['upper']
        sd = [((y[i]-mean[i])/2) for i in range(len(x))]
        limit = [ mean[i] + sd[i] * self.limit for i in range(len(x))]
        #map(list(zip())) awesomeness courtesy of
        #http://stackoverflow.com/questions/5520310/join-two-lists-by-interleaving
        return (map(list, zip(x, limit)))
    def chart_lln(self):
        x = self.bsa_arr if self.use_bsa else self.wt_arr
        mean = self.bsaData['mean'] if self.use_bsa else self.wtData['mean']
        y = self.bsaData['lower'] if self.use_bsa else self.wtData['lower']
        sd = [((mean[i]-y[i])/2) for i in range(len(x))]
        limit = [ mean[i] - sd[i] * self.limit for i in range(len(x))]
        return (map(list, zip(x, limit)))
# 
# individual site data 
#
lvedd_mm = { 'name': 'lvedd_mm',
        'bsaData': {
            'mean': [53.4, 46.8, 45.4, 43.3, 42.4, 41.7, 39.4, 38.5, 37.1, 35.8, 33.9, 33.2, 31.6, 31, 29, 27.1, 26, 23.6, 22.9, 21.2, 20],
            'lower': [45.4, 36.8, 39.0, 37.3, 35.8, 35.5, 32.5, 31.7, 31.0, 29.6, 27.4, 27.2, 26.0, 25.6, 23.4, 22.0, 21.0, 19.0, 18.0, 17.0, 16.4],
            'upper': [61.4, 54.8, 51.8, 49.3, 49.0, 47.9, 46.3, 45.3, 43.2, 42.0, 40.4, 39.2, 37.2, 36.4, 34.6, 32.1, 31.0, 27.2, 25.8, 25.4, 23.6]
        },
        'wtData': {
            'mean': [19.9, 18.8, 18.2, 18.1, 17.1],
            'lower': [16.5, 15.4, 15.1, 15.0, 15.0],
            'upper': [23.3, 22.2, 21.3, 21.1, 19.2]
        }
}
rvawd_mm = {'name': 'rvawd_mm',
          'bsaData': {
              'mean': [3.1, 3.1, 3.1, 3.0, 3.0, 2.9, 2.9, 2.8, 2.8, 2.8, 2.8, 2.8, 2.8, 2.75, 2.75, 2.75, 2.7, 2.7, 2.7, 2.6, 2.6],
              'lower': [1.9, 1.9, 1.9, 1.9, 1.9, 1.8, 1.8, 1.7, 1.7, 1.7, 1.7, 1.7, 1.7, 1.65, 1.65, 1.65, 1.6, 1.6, 1.6, 1.4, 1.4],
              'upper': [4.3, 4.3, 4.3, 4.1, 4.1, 4.0, 4.0, 3.9, 3.9, 3.9, 3.9, 3.9, 3.9, 3.85, 3.85, 3.85, 3.8, 3.8, 3.8, 3.8, 3.8]
          },
          'wtData': {
              'mean': [2.6, 2.6, 2.5, 2.5, 2.4],
              'lower': [1.5, 1.5, 1.4, 1.4, 1.3],
              'upper': [3.7, 3.7, 3.6, 3.6, 3.5]
          }
}

rvd_mm = { 'name': 'rvd_mm',
       'bsaData': {
        'mean': [17.5, 16.5, 15.6, 14, 13.5, 12.4, 11.8, 11.2, 11, 10.5, 10.1, 9.9, 9.6, 9.5, 9.3, 9, 8.9, 8.8, 8.7, 8.7, 8.7],
        'lower': [11.5, 10.3, 10.0, 9.0, 8.5, 7.6, 7.4, 6.4, 6.4, 5.8, 5.7, 5.5, 5.2, 5.0, 4.8, 4.5, 4.4, 4.3, 4.2, 4.2, 4.2],
        'upper': [23.5, 22.7, 21.2, 19.0, 18.5, 17.2, 16.2, 16.0, 15.6, 15.2, 14.5, 14.3, 14.0, 14.0, 13.8, 13.5, 13.4, 13.3, 13.2, 13.2, 13.2]
    },
    'wtData': {
        'mean': [8.6, 8.6, 8.5, 8.4, 8.4],
        'lower': [4.1, 4.1, 4.1, 4.0, 4.0],
        'upper': [13.1, 13.1, 12.9, 12.8, 12.8]
    }
}
ivsd_mm = { 'name': 'ivsd_mm',
        'bsaData': {
            'mean': [9.3, 8, 7.4, 6.7, 6.6, 6.5, 6.2, 5.8, 5.6, 5.2, 5, 4.8, 4.8, 4.6, 4.3, 4.2, 4.1, 3.9, 3.9, 3.8, 3.8],
            'lower': [6.8, 5.6, 5.2, 4.9, 4.8, 4.7, 4.3, 4.0, 3.8, 3.6, 3.5, 3.3, 3.3, 3.1, 2.7, 2.6, 2.6, 2.5, 2.5, 2.4, 2.4],
            'upper': [11.8, 10.4, 9.6, 8.5, 8.4, 8.3, 8.1, 7.6, 7.4, 6.8, 6.5, 6.3, 6.3, 6.1, 5.9, 5.8, 5.6, 5.3, 5.3, 5.2, 5.2]
        },
        'wtData': {
            'mean': [3.8, 3.7, 3.6, 3.5, 3.5],
            'lower': [2.4, 2.3, 2.3, 2.1, 2.1],
            'upper': [5.2, 5.1, 4.9, 4.7, 4.7]
        }
}
ivss_mm = { 'name': 'ivss_mm',
        'bsaData': {
            'mean': [10.3, 9.8, 9.5, 9.2, 9.0, 9.0, 9.0, 8.4, 8.3, 7.5, 7.2, 6.9, 6.9, 6.8, 6.6, 6.3, 6.2, 5.8, 5.8, 5.4, 5.2],
            'lower': [6.5, 5.8, 5.8, 5.8, 5.4, 5.4, 5.4, 5.1, 4.9, 4.4, 4.2, 3.8, 3.8, 3.7, 3.5, 3.3, 3.2, 3.0, 3.0, 2.6, 2.5],
            'upper': [14.1, 13.8, 13.2, 12.6, 12.6, 12.6, 12.6, 11.7, 11.7, 10.6, 10.2, 10.0, 10.0, 9.9, 9.7, 9.3, 9.2, 8.6, 8.6, 8.2, 7.9]
        },
        'wtData': {
            'mean': [5.4, 5.3, 5.1, 5.0, 4.4],
            'lower': [2.6, 2.5, 2.5, 2.4, 2.4],
            'upper': [8.2, 8.1, 7.7, 7.6, 6.4]
        }
}
lvesd_mm = { 'name': 'lvesd_mm',
        'bsaData': {
            'mean': [34.4, 29.8, 28.6, 27.6, 27.1, 27.1, 25.2, 24.4, 23.6, 22.7, 21.3, 20.4, 19.9, 19.3, 18, 17, 16.1, 14.8, 14.8, 13.6, 13.2],
            'lower': [25.6, 23.4, 22.5, 22.0, 21.5, 21.5, 19.6, 18.6, 18.0, 17.7, 16.1, 15.7, 15.4, 15.0, 14.0, 13.0, 12.0, 10.8, 10.8, 10.4, 10.2],
            'upper': [43.2, 36.2, 34.7, 33.2, 32.7, 32.7, 30.8, 30.2, 29.2, 27.7, 26.5, 25.1, 24.4, 23.6, 22.0, 21.0, 20.1, 18.8, 18.8, 16.8, 16.2]
        },
        'wtData': {
            'mean': [12.7, 11.9, 11.7, 11.7, 11.0],
            'lower': [10.2, 9.5, 9.2, 9.2, 9.7],
            'upper': [15.2, 14.3, 14.2, 14.2, 12.3]
        }
}
lvpwd_mm = { 'name': 'lvpwd_mm',
        'bsaData': {
            'mean': [8.1, 8.1, 7.7, 6.9, 6.9, 6.6, 6.3, 5.9, 5.9, 5.7, 5.2, 4.9, 4.8, 4.8, 4.6, 4.6, 4.2, 4.1, 4.1, 3.8, 3.6],
            'lower': [5.1, 5.1, 4.9, 4.3, 4.3, 4.0, 3.9, 3.7, 3.7, 3.6, 3.5, 3.4, 3.3, 3.3, 3.1, 3.1, 2.9, 2.8, 2.8, 2.7, 2.6],
            'upper': [11.1, 11.1, 10.5, 9.5, 9.5, 9.2, 8.7, 8.1, 8.1, 7.8, 6.9, 6.4, 6.3, 6.3, 6.1, 6.1, 5.5, 5.4, 5.4, 4.9, 4.6]
        },
        'wtData': {
            'mean': [3.7, 3.6, 3.5, 3.2, 2.7],
            'lower': [2.6, 2.5, 2.4, 2.2, 1.9],
            'upper': [4.8, 4.7, 4.6, 4.2, 3.5]
        }
}
lvpws_mm = { 'name': 'lvpws_mm',
        'bsaData': {
            'mean': [14.2, 12.8, 12.0, 11.5, 11.0, 10.7, 10.3, 9.5, 9.5, 9.1, 8.7, 8.2, 8.0, 8.0, 7.5, 7.3, 6.8, 6.6, 6.3, 5.9, 5.7],
            'lower': [9.9, 9.5, 8.5, 8.5, 8.1, 7.6, 7.0, 6.8, 6.8, 6.2, 6.1, 5.8, 5.7, 5.7, 5.2, 5.0, 4.5, 4.4, 4.2, 3.9, 3.7],
            'upper': [18.8, 16.1, 15.5, 14.5, 13.9, 13.8, 13.6, 12.2, 12.2, 12.0, 11.3, 10.6, 10.3, 10.3, 9.8, 9.6, 9.1, 8.8, 8.4, 7.9, 7.7]
        },
        'wtData': {
            'mean': [5.7, 5.4, 5.1, 5.0, 4.5],
            'lower': [3.5, 3.3, 3.1, 2.9, 2.8],
            'upper': [7.9, 7.5, 7.1, 7.1, 6.2]
        }
}
la_mm = { 'name': 'la_mm',
        'bsaData': {
            'mean': [32.5, 30.4, 29.9, 28.2, 27.3, 26.0, 25.2, 25.0, 23.2, 22.5, 21.2, 20.8, 20.1, 19.7, 18.7, 17.8, 16.8, 16.3, 15.3, 15.1, 14.0],
            'lower': [23.7, 23.8, 23.7, 22.8, 21.7, 20.9, 19.5, 19.2, 17.0, 16.5, 16.2, 16.1, 16.1, 15.3, 14.5, 13.8, 13.0, 12.0, 11.5, 11.5, 10.5],
            'upper': [41.3, 37.0, 36.1, 33.6, 32.9, 31.1, 30.9, 30.8, 29.4, 28.5, 26.2, 25.5, 24.1, 24.1, 22.9, 21.8, 20.6, 20.6, 19.1, 18.7, 17.5]
        },
        'wtData': {
            'mean': [13.7, 13.2, 12.6, 12.1, 11.5],
            'lower': [10.5, 10.2, 9.4, 8.5, 8.3],
            'upper': [16.9, 16.2, 15.8, 15.6, 14.7]
        }
    }

sites = [
    'rvawd_mm', 'rvd_mm', 'ivsd_mm', 'lvedd_mm', 'lvpwd_mm', 'ivss_mm', 'lvesd_mm', 'lvpws_mm', 'la_mm'
    ]


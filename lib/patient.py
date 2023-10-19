#!/usr/bin/env python
'''patient- a module that handles generic patient-related classes 

'''
from __future__ import division
import math
class Patient(object):
    '''a generic patient class; 
    
    '''
    def bsa(self, method='Haycock'):
        '''
        calculate BSA by various methods
        '''
        method = method.lower()
        if hasattr(self, 'ht') and hasattr(self, 'wt'):
            if method == 'haycock':
                return 0.024265 * math.pow(float(self.ht), 0.3964) * math.pow(float(self.wt), 0.5378)
            elif method == 'dubois':
                return 0.007184 * math.pow(float(self.ht), 0.725) * math.pow(float(self.wt), 0.425)
            elif method == 'boyd':
                wt = float(self.wt) * 1000 #converts kg to grams
                exponent = 0.7285 - 0.0188 * math.log10(wt)
                return 0.0003207 * math.pow(float(self.ht), 0.3) * math.pow(wt, exponent)
            elif method == 'mosteller':
                return math.sqrt( (float(self.ht) * float(self.wt) ) / 3600)
            elif method == 'gehan':
                return 0.0235 * math.pow(float(self.ht), 0.42246) * math.pow(float(self.wt), 0.51456)
            elif method == 'dreyer':
                return 0.1 * math.pow(float(self.wt), (2 / 3))
        else:
            #no ht or wt
            return None
    
    def bmi(self):
        if self.ht and self.wt:
            ht = float(self.ht)
            wt = float(self.wt)
            return wt / math.pow((ht / 100), 2);
        else:
            #no ht or wt
            return None

#!/usr/bin/env python

import webapp2
import views
import logging
import math
from calcs.exercise import config, blanchard_msse_2018
from lib.patient import Patient
from lib import who_bmi





class CPETandler(views.BaseHandler):
    def get(self):
        this_ref = 'blanchard-msse-2018'
        # logging.info(this_ref)
        try:
            ref = config.REFS['blanchard-msse-2018']
            # logging.info(ref)
        except:
            webapp2.abort(404)
        self.render_template('/refs/cpet.html',
                             page={"title": "Cardiopulmonary Exercise Testing Z-Score Calculator",
                                   "description": "CPET reference values according to Blanchard et al., MSSE 2018"},
                            action = this_ref,
                            ref = ref,
                            meas = config.INPUTS,
                            nav = None,
                            current_page = None)


class CalcHandler(views.JSONBaseHandler):
    '''
    the AJAX back end for calculating z-scores
    takes a form containing demographic, reference, and measurement data
    at various stages of completeness; BSA and range data may be calculated
    and returned before actual z-scores.
    '''

    def get(self):  # testing with GET; could also go with POST for production
        params = {}
        result = {}
        result['sites'] = {}
        # get all the form data
        for field in self.request.arguments():
            # str.replace(old, new[, count]) attempt at allowing commas
            params[field] = self.request.get(field).replace(',', '.', 1)
            # build a patient
        pt = Patient()
        for field in params:
            if params[field] != '':
                setattr(pt, field, params[field])

        # get the reference object/Base
        module = blanchard_msse_2018
        # logging.info('***module: %s ***' %module)
        Base = module.Base

        # iterate through the supplied measurements/sites
        # and return: BSA (if used); range and z-score for each
        for site in module.sites:
            if hasattr(pt, site):
                this_ref = Base(getattr(module, site), pt, config.zLimit)
                result['sites'][site] = {
                    'id': site,
                    'mean': this_ref.mean(),
                    'uln': this_ref.uln(),
                    'lln': this_ref.lln(),
                    'zscore': this_ref.zscore()
                }
        result['success'] = 'success'
        result['name'] = module.name
        result['citation'] = module.citation
        result['constraints'] = module.constraints
        if 'bsa' in module.required:
            result['bsaMethod'] = module.bsaMethod
            result['bsa'] = pt.bsa(module.bsaMethod)
        # new stuff for BMI and related calcs
        bmi = pt.bmi()
        result['bmi'] = round(bmi, 3)

        age = float(pt.age)
        if age > 5.0 and age < 19.0:
            bmiz = who_bmi.getBMIZscore(pt)
            result['bmiz'] = round(bmiz, 3)

            if bmiz > 1.04: #OVERWEIGHT 1.036 = 85%-ile; 1.65 = 95%-ile
                # calculate 85th percentile bmi and expected weight

                ht = float(pt.ht) / 100
                bmiAtCentile = who_bmi.getBMICentile(pt, '85')
                result['bmiAtCentile'] = (round(bmiAtCentile, 3))
                result['correctedWt'] = bmiAtCentile * ht * ht

            if bmiz  <=1.04:
                # no alternate analysis suggested...
                result['correctedWt'] = pt.wt
                result['bmiAtCentile'] = 'N/A'


        else:
            result['bmiz'] = 'N/A'
            result['bmiAtCentile'] = 'N/A'
            result['correctedWt'] = 'N/A'

        self.renderJSON(result)


class BMICalcHandler(views.JSONBaseHandler):
    '''
    the AJAX back end for calculating BMI, BMI Z-Score, and adjustedments
    '''

    def get(self):  # testing with GET; could also go with POST for production
        params = {}
        result = {}
        for field in self.request.arguments():
            # str.replace(old, new[, count]) attempt at allowing commas
            params[field] = self.request.get(field).replace(',', '.', 1)
        # build a patient
        pt = Patient()
        for field in params:
            if params[field] != '':
                setattr(pt, field, params[field])

        if float(pt.age) < 2.0:
            self.renderJSON({'notice': 'BMI data not available for age < 2 yrs'})
            return

        bmi = pt.bmi()
        result['bmi'] = round(bmi, 1)

        bmiz = who_bmi.getBMIZscore(pt)
        result['bmiz'] = round(bmiz,3)

        if bmiz > 1.3:
            # calculate 85th percentile bmi and expected weight
            result['centile'] = 85
            bmiAtCentile = who_bmi.getBMICentile(pt, '85')
            result['bmiAtCentile'] = round(bmiAtCentile, 3)
            ht = float(pt.ht) / 100

            alternateWt = bmiAtCentile * ht * ht

            result['alternateWt'] = round(alternateWt, 3)

            self.renderJSON(result)
            return

        if bmiz < -1.3:
            # calculate 15th percentile bmi and expected weight
            result['centile'] = 15
            bmiAtCentile = who_bmi.getBMICentile(pt, '15')
            result['bmiAtCentile'] = round(bmiAtCentile, 3)
            ht = float(pt.ht) / 100

            alternateWt = bmiAtCentile * ht * ht

            result['alternateWt'] = round(alternateWt, 3)

            self.renderJSON(result)
            return


        if bmiz >= -1.3 and bmiz <= 1.3:
            # no alternate analysis suggested...
            result['centile'] = 'N/A'

            result['bmiAtCentile'] = 'N/A'

            result['alternateWt'] = 'N/A'

            self.renderJSON(result)
            return
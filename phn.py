#!/usr/bin/env python

import webapp2
import views
import logging
import math
from calcs.echo import config, lopez_circimaging_2017
from lib.patient import Patient
from lib import cdc_bmi


class PHNHandler(views.BaseHandler):
    def get(self):
        this_ref = 'lopez-circimaging-2017'
        # logging.info(this_ref)
        try:
            ref = config.REFS['lopez-circimaging-2017']
            # logging.info(ref)
        except:
            webapp2.abort(404)
        self.render_template('/refs/phn.html',
                             page={"title": "THE PHN Z-Score Calculator",
                                   "description": "PHN data plus a reasonable way of dealing with over/underweight patients"},
                            action = this_ref,
                            ref = ref,
                            meas = config.MEASUREMENTS,
                            nav = config.REFS,
                            current_page = None)


class CalcHandler(views.JSONBaseHandler):
    '''
    the AJAX back end for calculating echo z-scores
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
        module = lopez_circimaging_2017
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
        if age > 2.0 and age < 20.0:
            bmiz = cdc_bmi.getBMIZscore(pt)
            result['bmiz'] = round(bmiz, 3)

            if bmiz > 1.65:
                # OBESE - greater than the 95%-1le
                result['description'] = 'obese'
                ht = float(pt.ht) / 100
                suggested = ['95', '85', '75', '50']
                temp = []
                for cent in suggested:
                    # create list with centile, bmi at that centile, weight at that bmi
                    l = []
                    l.append(cent)
                    bmiAtCentile = cdc_bmi.getBMICentile(pt, cent)
                    l.append(round(bmiAtCentile, 3))
                    alternateWt = bmiAtCentile * ht * ht
                    l.append(round(alternateWt, 3))
                    temp.append(l)
                result['alternativeData'] = temp


            if bmiz > 1.04 and bmiz <= 1.65: #OVERWEIGHT 1.036 = 85%-ile; 1.65 = 95%-ile
                # calculate 85th percentile bmi and expected weight
                result['description'] = 'overweight'
                ht = float(pt.ht) / 100
                suggested = ['85', '75', '50']
                temp = []
                for cent in suggested:
                    # create list with centile, bmi at that centile, weight at that bmi
                    l = []
                    l.append(cent)
                    bmiAtCentile = cdc_bmi.getBMICentile(pt, cent)
                    l.append(round(bmiAtCentile, 3))
                    alternateWt = bmiAtCentile * ht * ht
                    l.append(round(alternateWt, 3))
                    temp.append(l)
                result['alternativeData'] = temp

            if bmiz < -1.04:
                # calculate 15th percentile bmi and expected weight
                result['description'] = 'underweight'
                ht = float(pt.ht) / 100
                suggested = ['15', '50']
                temp = []
                for cent in suggested:
                    # create list with centile, bmi at that centile, weight at that bmi
                    l = []
                    l.append(cent)
                    bmiAtCentile = cdc_bmi.getBMICentile(pt, cent)
                    l.append(round(bmiAtCentile, 3))
                    alternateWt = bmiAtCentile * ht * ht
                    l.append(round(alternateWt, 3))
                    temp.append(l)
                result['alternativeData'] = temp

            if bmiz >= -1.04 and bmiz <=1.04:
                # no alternate analysis suggested...
                result['centile'] = 'N/A'
                result['bmiAtCentile'] = 'N/A'
                result['alternateWt'] = 'N/A'
                result['alternativeData'] = 'N/A'

        else:
            result['bmiz'] = 'N/A'
            result['centile'] = 'N/A'
            result['bmiAtCentile'] = 'N/A'
            result['alternateWt'] = 'N/A'

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

        bmiz = cdc_bmi.getBMIZscore(pt)
        result['bmiz'] = round(bmiz,3)

        if bmiz > 1.3:
            # calculate 85th percentile bmi and expected weight
            result['centile'] = 85
            bmiAtCentile = cdc_bmi.getBMICentile(pt, '85')
            result['bmiAtCentile'] = round(bmiAtCentile, 3)
            ht = float(pt.ht) / 100

            alternateWt = bmiAtCentile * ht * ht

            result['alternateWt'] = round(alternateWt, 3)

            self.renderJSON(result)
            return

        if bmiz < -1.3:
            # calculate 15th percentile bmi and expected weight
            result['centile'] = 15
            bmiAtCentile = cdc_bmi.getBMICentile(pt, '15')
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
#!/usr/bin/env python

import webapp2
import views
from calcs.cmr import config
from lib.patient import Patient
from collections import OrderedDict
import logging



class indexHandler(views.BaseHandler):
  def get(self):
    self.render_template('cmr-index.html',
      page= {'title': 'Cardiac MRI Z-Scores',
             'description': 'Z-score calculators for pediatric cardiac MRI',
             'keywords': 'pediatric cardiac MRI z score calculator pulmonary artery aorta lv volume mass'},
      refs = config.REFS,
      current_page = None
      )

class RefHandler(views.BaseHandler):
  def get(self, ref):
    this_ref = ref.lower()
    #logging.info(this_ref)
    try:
      ref = config.REFS[ref]
      #logging.info(ref)
    except:
      webapp2.abort(404)
      
    self.render_template('/refs/cmr-ref.html',
      page= {'title': ref.name,
             'description': ref.description,
             'keywords': ref.keywords},
      action= this_ref,
      ref = ref,
      meas = ref.inputs,
      nav = None,
      current_page = None
      )



class CalcHandler(views.JSONBaseHandler):
  '''
  the AJAX back end for calculating echo z-scores
  takes a form containing demographic, reference, and measurement data
  at various stages of completeness; BSA and range data may be calculated
  and returned before actual z-scores.
  '''
  def get(self, ref): #testing with GET; could also go with POST for production
    params = {}
    result = {}
    result['sites'] = {}
    #get all the form data
    for field in self.request.arguments():
        #str.replace(old, new[, count]) attempt at allowing commas
        params[field] = self.request.get(field).replace(',', '.', 1) 
    # build a patient
    pt = Patient()
    for field in params:
      if params[field] != '':
        setattr(pt, field, params[field])

    #get the reference object/Base
    module = config.REFS[ref]
    #logging.info('***module: %s ***' %module)
    Base = module.Base
    
    #iterate through the supplied measurements/sites
    #and return: BSA (if used); range and z-score for each
    for site in module.sites:
      if hasattr(pt, site):
        this_ref = Base(getattr(module, site), pt, config.zLimit)
        result['sites'][site]= {
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
    
    self.renderJSON(result)
  

def validInput(input, params):
    status = True
    if input in ['ht', 'wt', 'age']: #these are the common numeric variables
        try:
            float(params[input])
        except:
            status = False
    elif input == 'gender':
        gender = params['gender'].lower()
        if not (gender == 'm' or gender == 'f'):
            status = False
    return status


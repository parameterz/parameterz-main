#!/usr/bin/env python

import webapp2
import views
from calcs.echo import config
from lib.patient import Patient
import logging


class RefsHandler(views.BaseHandler):
  def get(self):
    self.render_template('/refs/index.html',
      page= {'title': 'Z-Score References',
             'description': '''a listing of publications that provide a
             manner of calculating a zscore for pediatric echo measurements'''},
      nav = config.REFS,
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
      
    self.render_template('/refs/ref.html',
      page= {'title': ref.name,
             'description': ref.description},
      action= this_ref,
      ref = ref,
      meas = config.MEASUREMENTS,
      nav = config.REFS,
      current_page = this_ref
      )

class SiteHandler(views.BaseHandler):
  def get(self, site):
    #find the site from data
    try:
      data = SITES[site]
    except:
      webapp2.abort(404)
    if site == 'lv-mass':
      self.render_template('/sites/lv-mass.html',
                           page = {'title': data['title'],
                                   'description': data['description']},
                           data = data,
                           meas = config.MEASUREMENTS,
                           nav = SITES,
                           current_page = site)
    else:
      self.render_template('/sites/site.html',
                           page = {'title': data['title'],
                                   'description': data['description']},
                           data = data,
                           meas = config.MEASUREMENTS,
                           nav = SITES,
                           current_page = site)


class SitesHandler(views.BaseHandler):
  def get(self):
    '''the "sites" home page'''
    self.render_template('/sites/index.html',
                         page={'title': 'Anatomic Sites',
                               'description': '2D echo z-score calulators listed by available anatomic groups.'},
                         nav = SITES,
                         current_page = None)


class MethodsHandler(views.BaseHandler):
  '''detailed listing of measurement methodolgy'''
  def get(self):
    self.render_template('methods.html',
      page= {'title': 'Methods' ,
             'description': 'Descriptions of the echo measurement methodology as applied to z-score calculations.',
             'keywords': 'echo, measurement, technique'
            },
      meas = config.MEASUREMENTS
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

def findRefs(list):
  '''return a list of refs that provide at least one of the sites in a given list'''
  temp = []
  for k,v in config.REFS.items():
    for item in list:
        if not hasattr(v, 'omitFromSites'): # specifically added to omit the Quezada ref from other ao root refs
            if item in v.sites:
                temp.append((v.name, k))
  temp = set(temp)
  return sorted(temp)
    
  

SITES = {
  'aortic-root': {
    'title': 'Aortic Root',
    'description': '2D echo z-scores of the aortic valve, sinuses of Valsalva, ST-junction, and ascending aorta',
    'intro': '''Calculate and compare z-scores of the aortic root using data from multiple references.
              References included conform to ASE _Pediatric_ Guideline methodology:
              measurements are made in systole, from inside edge to inside edge.
              Commonly used in the evaluation of patients with Marfan syndrome, Kawasaki disease,
              and patients with a bicuspid aortic valve.''',
    'sites': ['aov', 'sov', 'stj', 'aao'],
    'refs': findRefs(['aov', 'sov', 'stj', 'aao'])
  },
    'aortic-arch': {
    'title': 'Aortic Arch',
    'description': 'Z-scores of the aortic arch and isthmus',
    'intro': '''Calculate and compare z-scores of the aortic arch, including the aortic isthmus.
              Data from multiple references including recent data particularly suited for infants
              with arch hypoplasia or coarctation.
              References included conform to ASE Guideline methodology:
              measurements are made in systole, from inside edge to inside edge. (See the
              [methods](/methods#prox_arch) page for further details.)''',
    'sites': ['prox_arch', 'mid_arch', 'dist_arch', 'isthmus', 'dao', 'abd_ao'],
    'refs': findRefs(['prox_arch', 'mid_arch', 'dist_arch', 'isthmus', 'dao', 'abd_ao'])
    },
  'valves': {
    'title': 'Valves',
    'description': 'Calculate z-scores of the mitral, tricuspid, aortic, and pulmonary valves',
    'intro': '''Compare z-score calculations of the cardiac valves using data from institutions
             in Detroit, Cincinnatti, Boston, Pisa and others. Measured from hinge point to hinge point;
             AV valves measured in diastole; semilunar valves in systole.''',
    'sites': ['mvd_l', 'tvd_l', 'aov', 'pv'],
    'refs': findRefs(['mvd_l', 'tvd_l', 'aov', 'pv'])
  },
  'pulmonary-arteries': {
    'title': 'Pulmonary Arteries',
    'description': 'Z-scores of the main and branch pulmonary arteries (MPA, RPA, LPA)',
    'intro': '''Pediatric echo z-score calculator for the main
                  pulmonary artery (MPA), right pulmonary
                  (RPA), and left pulmonary arteries (LPA). ''',
    'sites': ['mpa', 'rpa', 'lpa'],
    'refs': findRefs(['mpa', 'rpa', 'lpa'])
  },
  'coronary-arteries': {
    'title': 'Coronary Arteries',
    'description': 'Calculate z-scores of the coronary arteries: lmca, lad, and rca',
    'intro': '''Calculate and compare z-scores of the coronary arteries using the most recent
            data published from Quebec, Boston, and Washington, D.C. Particularly useful
            in patients with a concern for coronary artery involvement related to Kawasaki disease.''',
    'sites': ['lmca', 'lad', 'circ', 'prox_rca', 'mid_rca', 'dist_rca'],
    'refs': findRefs(['lmca', 'lad', 'circ', 'prox_rca', 'mid_rca', 'dist_rca'])
  },
  'm-mode': {
    'title': 'M-Mode',
    'description': 'M-mode z-scores of left ventricular diameters and mass; ivsd, lvedd, lvpwd, lvm',
    'intro': '''Use this z-score calculator to compare z-scores and normal values
              for m-mode measurments of the left ventricle, including LV mass
              z-scores, from multiple references.''',
    'sites': ['ivsd_mm', 'lvedd_mm', 'lvpwd_mm', 'ivss_mm', 'lvesd_mm', 'lvpws_mm', 'lvm_mm'],
    'refs': findRefs(['ivsd_mm', 'lvedd_mm', 'lvpwd_mm', 'ivss_mm', 'lvesd_mm', 'lvpws_mm', 'lvm_mm'])
  }
}
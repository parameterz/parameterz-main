import os
import webapp2
from webapp2_extras import jinja2
from jinja2 import Markup
from google.appengine.api import mail
import json
import config
import logging
import models
import random
import re

#  A webapp2/Jinja base handler
#  courtesy of Nick Johnson:
#  http://blog.notdot.net/2011/11/Migrating-to-Python-2-7-part-2-Webapp-and-templates

class BaseHandler(webapp2.RequestHandler):
  @webapp2.cached_property
  def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

  def render_template(self, filename, **template_args):
        template_args.update({ 'updated_on': config.lastUpdated })
        self.response.write(self.jinja2.render_template(filename, **template_args))

class JSONBaseHandler(webapp2.RequestHandler):
  def renderJSON(self, data):
    self.response.headers['Content-Type'] = 'application/json'   
    self.response.out.write(json.dumps(data))


class MainHandler(BaseHandler):
  def get(self):
    self.render_template('index.html',
      page= {'title': 'Home',
       'description': 'www.parameterZ.com is the home page on the web for pediatric echo z-score calculators'
      })


class disclaimerHandler(BaseHandler):
  def get(self):
    self.render_template('disclaimer.html',
      page= {'title': 'Disclaimer',
       'description': 'tl;dr: If you are basing your medical decisions on a free calculator you found on the internet and things go horribly wrong - you have no one to blame but yourself.'
      })


class AboutHandler(BaseHandler):
  def get(self):
    self.render_template('about.html',
      page= {'title': 'About',
       'description': 'about the site'
      })

  def post(self):
    #handle adding data to storage, sending email, redirecting to thanks page
    #get the form data
    name = self.request.get('name')
    email = self.request.get('email')
    comment = Markup(self.request.get('comment')).striptags()
    errors = []
    if name == '':
      errors.append("please enter a name")
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
      errors.append("please enter a valid email")
    if comment == '':
      errors.append("Ermm... form submitted but no comment?")
    if len(errors) > 0:
      #dump them back to the about page with errors
      return self.render_template('about.html',
        page= {'title': 'About',
         'description': 'about the site'
        },
        errors = errors,
        form = {'name': name, 'email': email, 'comment': comment})
    #save data
    contact = models.Contact()
    contact.name = name
    contact.email = email
    contact.comment = comment 
    try:
      contact.put()
    except:
      logging.info('error writing to datastore')
    #send mail
    #build an email object
    exclamation = random.choice(["Up your Nyquist!",
                                 "Page the tech!",
                                 "Point where I'm looking!",
                                 "Zoom on that!"])
    message = mail.EmailMessage(sender="parameterz.com <dan.dyar@gmail.com>",
                        subject="%s Another Parameter(z) contact form has been submitted!" %exclamation)
    message.to = config.MAIL_TO_ADDRESS
    message.body = 'Date: %s \n' %contact.date
    message.body += 'From: %s \n' %contact.name
    message.body += 'Email: %s \n' %contact.email
    message.body += '\n-------\n'
    message.body += 'Comment: %s \n\n\n' %contact.comment
    try:
      message.send()
    except:
      logging.info('error sending mail')
    
    #redirect
    self.redirect('/thanks')


class ThanksHandler(BaseHandler):
  def get(self):
    self.render_template('thanks.html',
      page= {'title': 'Thanks!',
       'description': ''
      })

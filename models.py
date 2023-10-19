#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from google.appengine.ext import db

class Contact(db.Model):
  """Models an individual Contact entry with a name, email, comment, and date."""
  name = db.StringProperty()
  email = db.EmailProperty()
  comment = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)

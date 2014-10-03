import os
import urllib
import datetime

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2
import logging

class User(ndb.Model):
    userID = ndb.StringProperty(required=True)
    access_token = ndb.StringProperty(required=True)

 class Post(ndb.Model):
    message = ndb.StringProperty(indexed=False)
    access_token = ndb.StringProperty(indexed=False)
   	userID = ndb.StringProperty(indexed=False)
    date_to_post = ndb.DateTimeProperty()
    date_created = ndb.DateTimeProperty(auto_now_add=True)
    status = ndb.StringProperty(default="TBP")
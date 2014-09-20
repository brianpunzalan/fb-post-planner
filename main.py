import os
import urllib
import urllib2
import datetime
import json

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import urlfetch

import jinja2
import webapp2
import logging


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/main.html')
        self.response.write(template.render())

    def post(self):
        #post = Post()
        self.response.write("<script>console.log('fbposthandler ....')</script>")
        message = self.request.get('message')
        access_token = self.request.get('access_token')
        userID = self.request.get('userID')
        
        self.response.write("<script>console.log('"+access_token+"')</script>")
        self.response.write("<script>console.log('"+message+"')</script>")
        self.response.write("<script>console.log('"+userID+"')</script>")

        url = "https://graph.facebook.com/v2.1/"+userID+"/feed"

        form_fields = {
            "method": "post",
            "message" : message,
            "access_token" : access_token
        }

        form_data = urllib.urlencode(form_fields)
        result = urlfetch.fetch(url=url,
            payload=form_data,
            method=urlfetch.POST,
        )
        
        if result.status_code == 200:
            self.response.write("<script>console.log("+access_token+")</script>")
            self.response.write("<script>alert('Successful')</script>")
        elif result.status_code == 400:
            self.response.write("<script>console.log("+access_token+")</script>")
            self.response.write("<script>alert('Not Successful')</script>")
        self.response.write(result.status_code);

        content = json.loads(result.content)



class Post(ndb.Model):
    message = ndb.StringProperty(indexed=False)
    access_token = ndb.StringProperty(indexed=False)
    userID = ndb.StringProperty(indexed=False)

class FBPostHandler(webapp2.RequestHandler):
    def post(self):
        #post = Post()
        self.response.write("<script>console.log('fbposthandler ....')</script>")
        message = self.request.get('message')
        access_token = self.request.get('access_token');
        userID = self.request.googleet('userID')
        
        form_fields = {
            "message" : message,
            "access_token" : access_token,
            "method": "post"
        }

        form_data = urllib.urlencode(form_fields)
        result = urlfetch.fetch(url=url,
            payload=form_data,
            method=urlfetch.POST,
        )

        self.response.write("<script>console.log('"+result+"'')</script>")

        content = json.loads(result.content)

        self.response.write("<script>console.log('"+content+"'')</script>")

        if(content.get('id')):
            self.response.write('<script>alert("POSTED");window.location.assign("/")</script>')
        elif content["error"]["error_user_title"]:
            self.response.write("<script>alert('"+content["error"]["error_user_title"]+"'); window.location.assign('/')</script>")
        else:
            self.response.write('<script>alert("An error occurred."); window.location.assign("/")</script>')

        #post.put()

        #self.redirect('/success')

class FBPostSuccessHandler(webapp2.RequestHandler):
    def get():
        template = JINJA_ENVIRONMENT.get_template('template/success.html')
        self.response.write(template.render())

application = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/fbpost', FBPostHandler),
], debug=True)
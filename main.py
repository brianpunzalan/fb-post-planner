import os
import urllib
import urllib2
import json

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import urlfetch

import jinja2
import webapp2
import logging

from datetime import datetime,timedelta

import sched
import time
import threading

# from models import Post
# from models import Users

FACEBOOK_APP_ID = "767075363357147"
FACEBOOK_APP_SECRET = "a9a299a90cd3398167680df4890a9f8f"
GRAPH_API_URL ="https://graph.facebook.com/v2.1"

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def post_to_facebook(data,id):
    form_data = urllib.urlencode(data)
    url = GRAPH_API_URL+"/"+id+"/feed"
    result = urlfetch.fetch(url=url,payload=form_data,method=urlfetch.POST)
    content = json.loads(result.content)
    return content

def short_to_long_lived(access_token,self):
    url = "https://graph.facebook.com/oauth/access_token"
    data = {
        "grant_type" : "fb_exchange_token",
        "fb_exchange_token": access_token,
        "client_id" : FACEBOOK_APP_ID,
        "client_secret" : FACEBOOK_APP_SECRET,
        
    }
    form_data = urllib.urlencode(data)
    result = urlfetch.fetch(url=url,payload=form_data,method=urlfetch.POST)

    return result.content

def decode_response(str):
    access_token = str.split("&")[0].split("=")[1]
    return {
        "access_token" : access_token,
    }
def post_to_object(post):
    data = {
            "method": "post",
            "message": post.message,
            "access_token" : post.access_token
        }
    return data
class PostToFBHandler(webapp2.RequestHandler):
    def post(self):
        data = {
                    "method": "post",
                    "message": self.request.get("message"),
                    "access_token": self.request.get("access_token")
                };
        post = Posts()
        post.message = self.request.get("message")
        post.access_token = "Team 3: "+self.request.get("access_token")
        post.user_id = self.request.get("userID")
        post.date_to_post = datetime.now()+ timedelta(hours=8) 
        content = post_to_facebook(data,self.request.get("userID"))
        if(content.get("id")):
           self.response.write('<script>alert("Message posted to facebook.");window.location.assign("/")</script>')
        elif content["error"]["error_user_title"]:
            self.response.write('<script>alert("'+content["error"]["error_user_title"]+'");window.location.assign("/")</script>')
        else:
            self.response.write('<script>alert("An error occured.");window.location.assign("/")</script>')

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/main.html')
        self.response.write(template.render())

    def post(self):
        post = Posts()

        post.user_id = self.request.get("userID")
        post.message = "Team 3: "+self.request.get("message")
        post.date_to_post = datetime.strptime(self.request.get("date_to_post"),'%m/%d/%Y %I:%M %p')
        access_token = self.request.get("access_token")
        request = short_to_long_lived(access_token,self)
        request = decode_response(request)
        post.access_token = request["access_token"]
        
        post.put()

        self.response.write('<script>alert("Post Scheduled");window.location.assign("/")</script>')
        # post = Post()
        # self.response.write("<script>console.log('fbposthandler ....')</script>")
        # message = self.request.get('message')
        # access_token = self.request.get('access_token')
        # userID = self.request.get('userID')

        # url = "https://graph.facebook.com/v2.1/"+userID+"/feed"

        # form_fields = {
        #     "method": "post",
        #     "message" : message,
        #     "access_token" : access_token
        # }

        # form_data = urllib.urlencode(form_fields)
        # result = urlfetch.fetch(url=url,
        #     payload=form_data,
        #     method=urlfetch.POST,
        # )
        
        # if result.status_code == 200:
        #     self.response.write("<script>alert('Successful')</script>")
        # elif result.status_code == 400:
        #     self.response.write("<script>alert('Not Successful')</script>")
        # self.response.write(result.status_code);

        # content = json.loads(result.content)

class ListPostHandler(webapp2.RequestHandler):
    def get(self,id):
        to_be_post = ndb.gql("Select * from Posts "+
            "Where user_id = :1 and status = 'TBP' ",id).bind()
        posted = ndb.gql("Select * from Posts "+
            "Where user_id = :1 and status = 'Posted' ",id).bind()
        template_values={
            "posts":to_be_post,
            "posted": posted
        }
        template = JINJA_ENVIRONMENT.get_template('templates/list.html')
        self.response.write(template.render(template_values))

class EditPostHandler(webapp2.RequestHandler):
    def get(self,id):
        post = Posts.get_by_id(long(id))
        date = post.date_to_post.strftime("%m/%d/%Y %I:%M %p")
        template_values = {
            "post" : post,
            "date" : date
        }
        template = JINJA_ENVIRONMENT.get_template('templates/edit.html')
        self.response.write(template.render(template_values))

    def post(self,id):
        post = Posts.get_by_id(long(id))
        post.message = self.request.get("message")
        post.date_to_post = datetime.strptime(self.request.get("date_to_post"),'%m/%d/%Y %I:%M %p')
        post.put()
        self.response.write("<script> alert('Edit Successful.');window.location.assign('/');</script>")

class DeleteHandler(webapp2.RequestHandler):
    def get(self,id):
        post = Posts.get_by_id(long(id))
        post.key.delete()
        self.response.write("<script> alert('Delete Successful.');window.location.assign('/');</script>")        

class PostAllScheduledPosts(webapp2.RequestHandler):
    def get(self):
        p = Posts()
        p.date_to_post = datetime.now()
        posts = Posts.query(ndb.AND(Posts.date_to_post <= datetime.now()+timedelta(hours=8),Posts.status=="TBP")).fetch()
        for post in posts:
            data = post_to_object(post)
            post_to_facebook(data,post.user_id)
            post.status="Posted"
            post.put()

class Posts(ndb.Model):
    user_id = ndb.StringProperty(required=True)
    access_token = ndb.StringProperty(required=True)
    message = ndb.StringProperty(required=True)
    date_to_post = ndb.DateTimeProperty()
    date_created = ndb.DateTimeProperty(auto_now_add=True)
    status = ndb.StringProperty(default="TBP")

application = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/list/(.*)',ListPostHandler),
    ('/post-now',PostToFBHandler),
    ('/edit/(.*)',EditPostHandler),
    ('/delete/(.*)',DeleteHandler),
    ('/task/post',PostAllScheduledPosts)
], debug=True)
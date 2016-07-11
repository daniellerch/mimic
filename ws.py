#!/usr/bin/python

import sys
import web 
import json
import cgitb    
import logging
from chatbot import chatbot

# Initialize logging
logging.basicConfig(level=logging.DEBUG,
   format='%(asctime)s %(levelname)s %(message)s',
   filename='/var/log/mimic.log', filemode='a+')  
  
cgitb.enable()  
 

# List of services   
urls = (   
   '/', 'index',
   '/chat', 'chat'
)
 
app = web.application(urls, globals())   
 
 
# Service implementation  
class index:    
   def GET(self, name=""):
      web.seeother('../ui/index.html')
 
class chat:   
   def POST(self):
      data = web.data()
      user_input=json.loads(data)
      logging.debug(user_input["text"])

      cb=chatbot()
      human_input=user_input["text"].decode("utf-8")
      response=cb.talk(human_input)

      return response

if __name__ == "__main__":
   app.run()    
   

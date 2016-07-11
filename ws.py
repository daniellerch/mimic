#!/usr/bin/python

import sys
import web 
import json
import cgitb    
import logging


sys.path.append('/data/mega/research/AI/mimic')

from chatbot import chatbot

logging.basicConfig(level=logging.DEBUG,
   format='%(asctime)s %(levelname)s %(message)s',
   filename='/var/log/mimic.log', filemode='a+')  
  
cgitb.enable()  
 
# List of services   
urls = (   
   '/', 'index',
   '/chat', 'chat',
   '/test1', 'test1',
   '/test2', 'test2' 
)
 
app = web.application(urls, globals())   
 
 
# Service implementation  
 

class index:    
   def GET(self, name=""):
      web.seeother('../ui/index.html')
 
class chat:   
   def POST(self, name=""):
      data = web.data()
      logging.debug(data)   
      #return "chat service: "+r
      #print data 

      cb=chatbot()
      human_input=data.decode("utf-8")
      response=cb.talk(human_input)

      return data  

class test1:    
   def GET(self, name=""):
      return "test1 service"   
 
class test2:    
   def GET(self, name=""):
      return "test2 service"   
 
if __name__ == "__main__":
   app.run()    
   

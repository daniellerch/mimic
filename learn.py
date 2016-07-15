#!/usr/bin/python

import sys
import glob
from language.chatbot import chatbot

if __name__ == '__main__':

   cb=chatbot()
   files=glob.glob("learn/*.text")

   cb.clean_memory()

   for fn in files:
      print "Reading", fn
      with open(fn) as f:
         lines = f.readlines()

      for l in lines:
         if l[:1]!='#': # ignore comments
            r=cb.talk(l)
            if r!="":
               print ">", l[:-1]
               print "<", r
         





#!/usr/bin/python

import sys
import glob
from chatbot import chatbot

if __name__ == '__main__':

   cb=chatbot()
   files=glob.glob("learn/*.fact")

   cb.clean_memory()

   for fn in files:
      print "Reading", fn
      with open(fn) as f:
         lines = f.readlines()

      for l in lines:
         if l[:1]!='#': # ignore comments
            print cb.talk(l)
         





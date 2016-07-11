#!/usr/bin/python

import sys
import glob
from language.chatbot import chatbot

if __name__ == '__main__':

   cb=chatbot()
   files=glob.glob("learning_packages/*.fact")

   cb.clean_memory()

   for fn in files:
      print "Reading", fn
      with open(fn) as f:
         lines = f.readlines()

      for l in lines:
         if l[:1]!='#': # ignore comments
            print cb.talk(l)
         





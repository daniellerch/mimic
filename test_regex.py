#!/usr/bin/python

import sys
import glob
import re

if __name__ == '__main__':

   files=glob.glob("learn/*.text")

   for fn in files:
      print "Reading", fn
      with open(fn) as f:
         lines = f.readlines()

      for l in lines:
         l=l[:-1]+"."
         print l
         m = re.search('(\w+) (\w+) (es|son) (\w+) (\w+).', l, re.UNICODE)
         if m:
            print "grp: ", m.group(2), ":", m.group(5)
         print "--"





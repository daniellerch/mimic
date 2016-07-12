#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from pattern.search import Pattern
from pattern.es import parsetree

t = parsetree('Pedro es mas feo que Juan.', lemmata=True)
t = parsetree('El Pedro fue mas alto y gordo que Juan.', lemmata=True)
#t = parsetree('Yo soy Sam.', lemmata=True)

p = Pattern.fromstring('{NP} ser mas {*} que {NP}')
try:
   m = p.match(t)
except:
   print sys.exc_info()
#print m
#print m.group(1)
#print m.group(2)
#print m.group(3)



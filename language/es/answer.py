#!/usr/bin/python
# -*- coding: utf-8 -*-

import random

class StandardAnswer:

   def __init__(self):
       
      self.ok_synonymous=[]
      self.ok_synonymous.append( u"De acuerdo" )
      self.ok_synonymous.append( u"Vale" )
      self.ok_synonymous.append( u"Genial!" )
      self.ok_synonymous.append( u"Muy bien" )
      self.ok_synonymous.append( u"Bien" )
      self.ok_synonymous.append( u"Perfecto" )
      self.ok_synonymous.append( u"Tomo nota" )
      self.ok_synonymous.append( u"Me lo apunto" )
      self.ok_synonymous.append( u"Estupendo" )
      self.ok_synonymous.append( u"Gracias por la información" )


   def get_ok_synonymous(self):
      rnd=random.randint(0, len(self.ok_synonymous)-1)
      return self.ok_synonymous[rnd]

#!/usr/bin/python
# -*- coding: utf-8 -*-


# Copyright (c) 2011-2013 University of Antwerp, Belgium

from pattern.es import singularize, pluralize, attributive, predicative
from pattern.es import MALE, FEMALE

definite_articles=["el", "la", "los", "las"]
indefinite_articles=["un", "uno", "una", "unos", "unas"]

is_a_relation=["es", "son"]

class Word():

   # {{{ __init__()
   def __init__(self, w):
      self.word = w.lower()
      self.is_singular=True
      self.is_masculine=True
      self.to_masculine()
      self.to_singular()
   # }}}

   # {{{ to_singular()
   def to_singular(self):
      self.word = singularize(self.word)
      self.is_singular=True
      return self
   # }}}

   # {{{ to_plural()
   def to_plural(self):
      self.word = pluralize(self.word)
      self.is_singular=False
      return self
   # }}}

   # {{{ to_feminine()
   def to_feminine(self):
      self.word = attributive(self.word, gender=FEMALE)

      if self.is_singular:
         self.to_singular()
      else:
         self.to_plural()

      self.is_masculine=False
      return self
   # }}}

   # {{{ to_masculine()
   def to_masculine(self):
      self.word = predicative(self.word)

      if self.is_singular:
         self.to_singular()
      else:
         self.to_plural()

      self.is_masculine=True
      return self
   # }}}


# Tes
if __name__ == '__main__':

   for string in ["perro", "mascotas", u"mamás", "pueril", "Juan", "Juana"]:
      w = Word(string)
      print w.to_masculine().to_singular().word
      print w.to_masculine().to_plural().word
      print w.to_feminine().to_singular().word
      print w.to_feminine().to_plural().word
      print "--"



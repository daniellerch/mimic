#!/usr/bin/python
# -*- coding: utf-8 -*-

import language.es.pattern_utils as pattern_utils
from pattern.es import parsetree, parse
from pattern.es import conjugate, lemma, lexeme, tenses
from pattern.es import singularize, pluralize, attributive, MALE, SINGULAR
from pattern.es import MALE, FEMALE

import random

class Answer:

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

   def get_question_reply(self, sentence_info, options):

      if len(options)==0:
         return "No lo se"

      if sentence_info['relation'] == 'IS-A':
         rnd=random.randint(0, len(options)-1)
         text="Es un "+options[rnd]
         # TODO: "un" must be checked
         return text

      if sentence_info['relation'] == 'HAS-ATTRIBUTE':
         rnd=random.randint(0, len(options)-1)

         for cnt in range(len(options)):
            if parsetree(options[rnd]).words[0].type[0:2]=='JJ':
               return "Es "+options[rnd]

      return "No lo se"




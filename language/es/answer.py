#!/usr/bin/python
# -*- coding: utf-8 -*-

import language.es.pattern_utils as pattern_utils
from pattern.es import parsetree, parse
from pattern.es import conjugate, lemma, lexeme, tenses
from pattern.es import singularize, pluralize, attributive, MALE, SINGULAR
from pattern.es import MALE, FEMALE
from knowledge import knowledge_base
import random

class Answer:

   def __init__(self):
       
      self.ok_synonymous=[
         u"De acuerdo",
         u"Vale",
         u"Genial!",
         u"Muy bien",
         u"Bien",
         u"Perfecto",
         u"Tomo nota",
         u"Me lo apunto",
         u"Estupendo",
         u"Gracias por la información",
         u"Interesante",
         u"Muy instructivo",
         u"Fantástico",
         u"Que bien"]

   def get_unknown_command():
      return u"No te he entendido. ¿Podrías reformular la frase?"

   def get_internal_error():
      return "Vaya, parece que tengo un problema interno"

   def get_ok_synonymous(self):
      rnd=random.randint(0, len(self.ok_synonymous)-1)
      return self.ok_synonymous[rnd]

   def get_question_reply(self, sentence_info, options):

      if len(options)==0:
         return "No lo se"

      if sentence_info['relation'] == 'IS-A':
         rnd=random.randint(0, len(options)-1)
         concept=knowledge_base.Concept(options[rnd])
         if concept.get_gender()=='f':
            text="Es una "+options[rnd]
         else:
            text="Es un "+options[rnd]
         return text

      if sentence_info['relation'] == 'HAS-ATTRIBUTE':
         rnd=random.randint(0, len(options)-1)

         for cnt in range(len(options)):
            if parsetree(options[cnt]).words[0].type[0:2]=='JJ':
               return "Es "+options[cnt]

      return "No lo se"




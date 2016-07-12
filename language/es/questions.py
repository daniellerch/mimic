#!/usr/bin/python
# -*- coding: utf-8 -*-

import language.es.structures as structures

# {{{ process()
def process(t):
   question=t.string[:-1].strip()
   question_list=["que es"]
   for q in question_list:
      if structures.strip_accents(question.lower()).startswith(q):
         q, n, p = structures.parse_NP(t.words[2:len(t.words)])
         r=dict()
         r['code']=0
         r['type']='query'
         r['relation']='IS-A'
         r['object']=n
         # TODO: process quantifier and properties
         return [r]

   return None
# }}}


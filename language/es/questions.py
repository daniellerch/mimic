#!/usr/bin/python
# -*- coding: utf-8 -*-

import language.es.pattern_utils as pattern_utils
from pattern.es import parsetree

# {{{ process()
def process(sentence):
   t = parsetree(sentence, lemmata=True)
   m=pattern_utils.pattern_match("que ser {NP}", t)
   if m:
      q, n, p = pattern_utils.parse_NP(m.group(1))
      r=dict()
      r['type']='query'
      r['question']='que'
      r['relation']='ser'
      r['object']=n
      return r

   m=pattern_utils.pattern_match("como ser {NP}", t)
   if m:
      q, n, p = pattern_utils.parse_NP(m.group(1))
      r=dict()
      r['type']='query'
      r['question']='como'
      r['relation']='ser'
      r['object']=n
      return r

   m=pattern_utils.pattern_match("que tener {NP}", t)
   if m:
      q, n, p = pattern_utils.parse_NP(m.group(1))
      r=dict()
      r['type']='query'
      r['question']='que'
      r['relation']='tener'
      r['object']=n
      return r



   return None
# }}}


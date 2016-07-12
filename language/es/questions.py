#!/usr/bin/python
# -*- coding: utf-8 -*-

import language.es.structures as structures

# {{{ process()
def process(t):
   m=structures.pattern_match("que ser {NP}", t)
   if m:
      q, n, p = structures.parse_NP(m.group(1))
      r=dict()
      r['type']='query'
      r['relation']='IS-A'
      r['object']=n
      return r

   m=structures.pattern_match("como ser {NP}", t)
   if m:
      q, n, p = structures.parse_NP(m.group(1))
      r=dict()
      r['type']='query'
      r['relation']='HAS-ATTRIBUTE'
      r['object']=n
      return r




   return None
# }}}


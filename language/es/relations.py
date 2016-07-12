#!/usr/bin/python
# -*- coding: utf-8 -*-

import language.es.structures as structures

# {{{ process()
def process(t, relation):

   if relation=='IS-A':
      return process_is_a(t)
  
   if relation=='IS-PROPERTY-OF':
      return process_is_property_of(t)
    
   return None
# }}}

# {{{ process_is_a()
def process_is_a(t):

   m=structures.pattern_match("{NP} ser {JJ*}", t)
   if not m: return None

   Aq, An, Aprop = structures.parse_NP(m.group(1))
   Bq, Bn, Bprop = structures.parse_NP(m.group(2))

   r=dict()

   if Aq!="exist": 
      Aq="all"
   if Bq!="exist": 
      Bq="all"

   r['code']=0
   r["type"]="relation"
   r["source_quantifier"]=Aq
   r["source"]=An
   r["destination_quantifier"]=Bq
   r["destination"]=Bn
   r["relation"]='IS-A'

   return [r]
# }}}

# {{{ process_is_property_of()
def process_is_property_of(t):

   while True:

      m=structures.pattern_match("{NP} pertenecer a {NP}", t)
      if m: break

      m=structures.pattern_match("{NP} ser propiedad de {NP}", t)
      if m: break

      m=structures.pattern_match("{NP} ser de {NP}", t)
      if m: break

      return None

   print m

   Aq, An, Aprop = structures.parse_NP(m.group(1))
   Bq, Bn, Bprop = structures.parse_NP(m.group(2))

   r=dict()
   r['code']=0
   r["type"]="relation"
   r["source_quantifier"]=Aq
   r["source"]=An
   r["destination_quantifier"]=Bq
   r["destination"]=Bn
   r["relation"]='PROPERTY-OF'

   return [r]
# }}}


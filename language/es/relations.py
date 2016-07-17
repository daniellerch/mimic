#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re
import language.es.pattern_utils as pattern_utils
import language.es.words as words


# {{{ process()
def process(t):

   r=process_has_attribute(t)
   if r: return r
  
   r=process_is_property_of(t)
   if r: return r
  
   r=process_is_part_of(t)
   if r: return r

   r=process_is_a(t)
   if r: return r

   r=process_contains(t)
   if r: return r


   return None
# }}}

# {{{ process_has_attribute()
def process_has_attribute(t):

   while True:

      m=pattern_utils.pattern_match("{NP} ser {JJ*}", t)
      if m: break

      return None

   print m

   Aq, An, Aprop = pattern_utils.parse_NP(m.group(1))
   Bq, Bn, Bprop = pattern_utils.parse_NP(m.group(2))

   r=dict()
   r['code']=0
   r["type"]="relation"
   r["source_quantifier"]=Aq
   r["source"]=An
   r["destination_quantifier"]=Bq
   r["destination"]=Bn
   r["relation"]='HAS-ATTRIBUTE'

   return r
# }}}

# {{{ process_is_property_of()
def process_is_property_of(t):

   while True:

      m=pattern_utils.pattern_match("{NP} pertenecer a {NP}", t)
      if m: break

      m=pattern_utils.pattern_match("{NP} ser propiedad de {NP}", t)
      if m: break

      m=pattern_utils.pattern_match("{NP} ser de {NP}", t)
      if m: break

      return None

   print m

   Aq, An, Aprop = pattern_utils.parse_NP(m.group(1))
   Bq, Bn, Bprop = pattern_utils.parse_NP(m.group(2))

   r=dict()
   r['code']=0
   r["type"]="relation"
   r["source_quantifier"]=Aq
   r["source"]=An
   r["destination_quantifier"]=Bq
   r["destination"]=Bn
   r["relation"]='PROPERTY-OF'

   return r
# }}}

# {{{ process_is_part_of()
def process_is_part_of(t):

   while True:

      m=pattern_utils.pattern_match("{NP} ser parte de {NP}", t)
      if m: break

      m=pattern_utils.pattern_match("{NP} formar parte de {NP}", t)
      if m: break

      return None

   print m

   Aq, An, Aprop = pattern_utils.parse_NP(m.group(1))
   Bq, Bn, Bprop = pattern_utils.parse_NP(m.group(2))

   r=dict()
   r['code']=0
   r["type"]="relation"
   r["source_quantifier"]=Aq
   r["source"]=An
   r["destination_quantifier"]=Bq
   r["destination"]=Bn
   r["relation"]='IS-PART-OF'

   return r
# }}}

# {{{ process_is_a()
def process_is_a(t):

   r=dict()
   r['code']=0

   dart="|".join(words.definite_articles)
   iart="|".join(words.indefinite_articles)
   relation="|".join(words.is_a)

   print t

   while True:
      # Un perro es un animal
      ms = '('+iart+'|'+dart+') (\w+) ('+relation+') ('+iart+') (\w+).'
      m = re.search(ms, t, re.UNICODE)
      if m: 
         a1, w1, a2, w2 = m.group(1), m.group(2), m.group(4), m.group(5)
         r["source_quantifier"]='all'
         r["destination_quantifier"]='all'
         break

      return None


   r["type"]="relation"
   r["source"]=w1
   r["destination"]=w2
   r["relation"]='IS-A'

   return r
# }}}

# {{{ process_contains()
def process_contains(t):

   while True:

      m=pattern_utils.pattern_match("{NP} contiene {NP}", t)
      if m: break

      m=pattern_utils.pattern_match("{NP} tener dentro {NP}", t)
      if m: break

      return None

   print m

   Aq, An, Aprop = pattern_utils.parse_NP(m.group(1))
   Bq, Bn, Bprop = pattern_utils.parse_NP(m.group(2))

   r=dict()
   r['code']=0
   r["type"]="relation"
   r["source_quantifier"]=Aq
   r["source"]=An
   r["destination_quantifier"]=Bq
   r["destination"]=Bn
   r["relation"]='CONTAINS'

   return r
# }}}





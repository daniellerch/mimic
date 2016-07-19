#!/usr/bin/python
# -*- coding: utf-8 -*-

import language.es.pattern_utils as pattern_utils



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

   m=pattern_utils.pattern_match("{NP} ser {JJ*}", t)
   if not m:
      return None

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

   m = ( pattern_utils.pattern_match("{NP} pertenecer a {NP}", t) or
         pattern_utils.pattern_match("{NP} ser propiedad de {NP}", t) or
         pattern_utils.pattern_match("{NP} ser de {NP}", t) )
   if not m: 
      return None

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

   m = ( pattern_utils.pattern_match("{NP} ser parte de {NP}", t) or
         pattern_utils.pattern_match("{NP} formar parte de {NP}", t) )
   if not m:
      return None

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

   m = ( pattern_utils.pattern_match("{NP} ser {NP}", t) or
         pattern_utils.pattern_match("{JJ*} ser {NP}", t) )

   if not m:
      return None


   Aq, An, Aprop = pattern_utils.parse_NP(m.group(1))
   Bq, Bn, Bprop = pattern_utils.parse_NP(m.group(2))

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

   return r
# }}}

# {{{ process_contains()
def process_contains(t):

   m = ( pattern_utils.pattern_match("{NP} contiene {NP}", t) or
         pattern_utils.pattern_match("{NP} tener dentro {NP}", t) )
   if not m:
      return None

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





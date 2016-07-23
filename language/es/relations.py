#!/usr/bin/python
# -*- coding: utf-8 -*-

import language.es.pattern_utils as pattern_utils
from pattern.es import parsetree, conjugate, INFINITIVE


# {{{ process()
def process(sentence):

    t = parsetree(sentence, lemmata=True)

    m = pattern_utils.pattern_match("{*} {VP} {*}", t)
    if not m:
        return None

    Aq, Ag, An, Aprop = pattern_utils.parse_NP(m.group(1))
    Bq, Bg, Bn, Bprop = pattern_utils.parse_NP(m.group(3))

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
    r['source_gender']=Ag
    r['destination_gender']=Bg
    r["relation"]=conjugate(m.group(2).string, INFINITIVE)


    return r
# }}}


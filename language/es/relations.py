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

    An, Ag, Anoun = pattern_utils.parse_NP(m.group(1))
    Bn, Bg, Bnoun = pattern_utils.parse_NP(m.group(3))

    r=dict()

    r['code']=0
    r["type"]="relation"
    r["source_quantifier"]=An
    r["source"]=Anoun
    r["destination_quantifier"]=Bn
    r["destination"]=Bnoun
    r['source_gender']=Ag
    r['destination_gender']=Bg
    r["relation"]=conjugate(m.group(2).string, INFINITIVE)


    return r
# }}}


#!/usr/bin/python
# -*- coding: utf-8 -*-

import language.es.pattern_utils as pattern_utils
from pattern.es import parsetree, conjugate, INFINITIVE

# {{{ process()
def process(sentence):
    t = parsetree(sentence, lemmata=True)
    m=pattern_utils.pattern_match("que {VP} {NP}", t)
    if m:
        q, g, n, p = pattern_utils.parse_NP(m.group(2))
        r=dict()
        r['type']='query'
        r['question']='que'
        r["relation"]=conjugate(m.group(1).string, INFINITIVE)
        r['gender']=g
        r['object']=n
        return r

    m=pattern_utils.pattern_match("como {VP} {NP}", t)
    if m:
        q, g, n, p = pattern_utils.parse_NP(m.group(2))
        r=dict()
        r['type']='query'
        r['question']='como'
        r["relation"]=conjugate(m.group(1).string, INFINITIVE)
        r['gender']=g
        r['object']=n
        return r

    return None
# }}}


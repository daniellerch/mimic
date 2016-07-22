#!/usr/bin/python
# -*- coding: utf-8 -*-

import language.es.pattern_utils as pattern_utils
from random import randint
from pattern.es import parsetree

# {{{ process()
def process(sentence):

    t = parsetree(sentence, lemmata=True)
    greeting=t.string.strip()

    greeting_list_q=["hola", "buenas"]
    greeting_list_a=["hola", "buenas"]
    if greeting.lower() in greeting_list_q:
        r=dict()
        r['code']=0
        r['type']='direct_answer'
        r['message']=greeting_list_a[randint(0,len(greeting_list_a)-1)]
        return r

    greeting_list_q=["que tal", "como estas", u"cómo estás", "como va",  
        "como te encuentras", "va todo bien"]
    greeting_list_a=["Estoy bien, gracias por preguntar"]
    if greeting.lower() in greeting_list_q:
        r=dict()
        r['code']=0
        r['type']='direct_answer'
        r['message']=greeting_list_a[randint(0,len(greeting_list_a)-1)]
        return r

    greeting_list_q=["buenos dias", "buenas tardes", "buenas noches"]
    greeting_list_a=["hola", "buenas"]
    if greeting.lower() in greeting_list_q:
        r=dict()
        r['code']=0
        r['type']='direct_answer'
        r['message']=greeting_list_a[randint(0,len(greeting_list_a)-1)]
        return r

    return None
# }}}



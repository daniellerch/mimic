#!/usr/bin/python
# -*- coding: utf-8 -*-

import knowledge.knowledge_base as knowledge_base
from language.es.answer import Answer
import language.es.pattern_utils as pattern_utils
import language.es.greetings as greetings
import language.es.questions as questions
import language.es.relations as relations




class chatbot:
 
	# {{{ __init__  
    def __init__(self, user='MASTER', lang='es'):
        self.kb=knowledge_base.knowledge_base()
        u=knowledge_base.Source(user)
        self.id_user=u.id
        self.lang=lang
    # }}}

    # {{{ clean_memory()
    def clean_memory(self):
        self.kb.clean()
    # }}}

    # {{{ talk()
    # Receives a message and returns an answer
    def talk(self, human_input):

        if human_input[-1:]!='.':
            human_input+='.'

        answer = Answer()

        sentence=human_input.lower()
        sentence=pattern_utils.sentence_pre_processing(sentence)

        sentence_info = ( greetings.process(sentence) or
                                questions.process(sentence) or
                                relations.process(sentence) )

        if not sentence_info:
            return answer.get_unknown_command()

        if sentence_info.has_key('code') and sentence_info["code"]!=0:
            return sentence_info["error_message"]

        if sentence_info["type"]=="relation":
            self.kb.add_2n_relation(
                self.id_user,     
                sentence_info["relation"], 
                sentence_info["source_quantifier"], 
                sentence_info["source"], 
                sentence_info["destination_quantifier"],
                sentence_info["destination"]
            )
            return answer.get_ok_synonymous()

        elif sentence_info["type"]=="query":
            results=self.kb.query_2n_relation(
                sentence_info["relation"], 
                sentence_info["object"]
            )
            return answer.get_question_reply(sentence_info, results)

        elif sentence_info["type"]=="direct_answer":
            return sentence_info["message"]


        return answer.get_internal_error()
    # }}}






from language.nlp import nlp
from knowledge.knowledge_base import knowledge_base
from language.es.answer import Answer
import logging


class chatbot:
 
	# {{{ __init__  
   def __init__(self):
      self.kb=knowledge_base()
      self.nlp=nlp()
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

      sentence_info=self.nlp.parse_sentence(human_input)
      answer = Answer()

      if sentence_info.has_key('code') and sentence_info["code"]!=0:
         return sentence_info["error_message"]

      if sentence_info["type"]=="relation":
         self.kb.add_2n_relation(
            0,    
            sentence_info["relation"], 
            sentence_info["source_quantifier"], 
            sentence_info["source"], 
            sentence_info["destination_quantifier"],
            sentence_info["destination"]
         )
         return answer.get_ok_synonymous()

      elif sentence_info["type"]=="query":
         results=self.kb.query_dst(
            sentence_info["relation"], 
            sentence_info["object"]
         )
         return answer.get_question_reply(sentence_info, results)

      elif sentence_info["type"]=="direct_answer":
         return sentence_info["message"]


      return "Vaya, parece que tengo un problema interno"
   # }}}





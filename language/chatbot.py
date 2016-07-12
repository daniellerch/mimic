
from language.nlp import nlp
from knowledge.knowledge_base import knowledge_base
from language.es.answer import StandardAnswer
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

      r=self.nlp.parse_sentence(human_input)

      if r["type"]=="relation":
         self.kb.add_2n_relation(
            0,    
            r["relation"], 
            r["source_quantifier"], 
            r["source"], 
            r["destination_quantifier"],
            r["destination"]
         )
         return StandardAnswer().get_ok_synonymous()

      elif r["type"]=="query":
         results=self.kb.query_dst(r["relation"], r["object"])
         return results

      elif r["type"]=="direct_answer":
         return r["message"]

      else:
         return "ERROR: unknown type", d["type"]

      return "ERROR: ?"
   # }}}






import aiml
from nlp import nlp
from knowledge_base import knowledge_base

class chatbot:
   
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

      data=self.nlp.parse_sentence(human_input)
      print data

      for d in data:
         if d["type"]=="relation":
            src=d["source"]
            dst=d["destination"]
            src_q=d["source_quantifier"]
            dst_q=d["destination_quantifier"]
            self.kb.add_2n_relation(0, d["relation"], src_q, src, dst_q, dst)
            return ""

         elif d["type"]=="query":
            entity=d["object"]
            results=self.kb.query_dst(d["relation"], entity)
            print results
            return ""

         elif d["type"]=="direct_answer":
            return d["message"]

         else:
            print "ERROR: unknown type", d["type"]
            return ""

      return "ERROR: ?"
   # }}}





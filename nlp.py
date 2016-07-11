#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
{{{ TAGS

http://www.clips.ua.ac.be/pages/mbsp-tags

Part-of-speech tags
^^^^^^^^^^^^^^^^^^^
Part-of-speech tags are assigned to a single word according to its role in the 
sentence. Traditional grammar classifies words based on eight parts of speech: 
the verb (VB), the noun (NN), the pronoun (PR+DT), the adjective (JJ), the 
adverb (RB), the preposition (IN), the conjunction (CC), and the interjection 
(UH).

Tag   Description + Example
==============================================================================
CC    conjunction, coordinating  and, or, but
CD    cardinal number   five, three, 13%
DT    determiner  the, a, these 
EX    existential there there were six boys 
FW    foreign word   mais 
IN    conjunction, subordinating or preposition of, on, before, unless 
JJ    adjective   nice, easy
JJR   adjective, comparative  nicer, easier
JJS   adjective, superlative  nicest, easiest 
LS    list item marker   
MD    verb, modal auxillary   may, should 
NN    noun, singular or mass  tiger, chair, laughter 
NNS   noun, plural   tigers, chairs, insects 
NNP   noun, proper singular   Germany, God, Alice 
NNPS  noun, proper plural  we met two Christmases ago 
PDT   predeterminer  both his children 
POS   possessive ending 's
PRP   pronoun, personal me, you, it 
PRP$  pronoun, possessive  my, your, our 
RB    adverb   extremely, loudly, hard  
RBR   adverb, comparative  better 
RBS   adverb, superlative  best 
RP    adverb, particle  about, off, up 
SYM   symbol   % 
TO    infinitival to what to do? 
UH    interjection   oh, oops, gosh 
VB    verb, base form   think 
VBZ   verb, 3rd person singular present   she thinks 
VBP   verb, non-3rd person singular present  I think 
VBD   verb, past tense  they thought 
VBN   verb, past participle   a sunken ship 
VBG   verb, gerund or present participle  thinking is fun 
WDT   wh-determiner  which, whatever, whichever 
WP    wh-pronoun, personal what, who, whom 
WP$   wh-pronoun, possessive  whose, whosever 
WRB   wh-adverb   where, when 
.     punctuation mark, sentence closer   .;?* 
,     punctuation mark, comma , 
:     punctuation mark, colon : 
(     contextual separator, left paren ( 
)     contextual separator, right paren   ) 


Chunk tags
^^^^^^^^^^
Chunk tags are assigned to groups of words that belong together (i.e. phrases).
The most common phrases are the noun phrase (NP, for example the black cat) 
and the verb phrase (VP, for example is purring).

Tag   Description                Words                Example
==============================================================================
NP    noun phrase                DT+RB+JJ+NN + PR     the strange bird
PP    prepositional phrase       TO+IN                in between
VP    verb phrase                RB+MD+VB             was looking
ADVP  adverb phrase              RB                   also
ADJP  adjective phrase           CC+RB+JJ             warm and cosy
SBAR  subordinating conjunction  IN                   whether or not
PRT   particle                   RP                   up the stairs
INTJ  interjection               UH                   hello

The IOB prefix marks whether a word is inside or outside of a chunk.


Tag   Description
==============================================================================
I-    inside the chunk
B-    inside the chunk, preceding word is part of a different chunk
O     not part of a chunk

A prepositional noun phrase (PNP) is a group of chunks starting with a 
preposition (PP) followed by noun phrases (NP), for example: under the table.

Tag   Description Chunks   Example
PNP   prepositional noun phrase  PP+NP as of today
Relation tags

Relations tags describe the relation between different chunks, and clarify the role of a chunk in that relation. The most common roles in a sentence are SBJ (subject noun phrase) and OBJ (object noun phrase). They link NP to VP chunks. The subject of a sentence is the person, thing, place or idea that is doing or being something. The object of a sentence is the person/thing affected by the action.

Tag   Description Chunks   Example  %
-SBJ  sentence subject  NP the cat sat on the mat
35
-OBJ  sentence object   NP+SBAR  the cat grabs the fish
27
-PRD  predicate   PP+NP+ADJP  the cat feels warm and fuzzy
7
-TMP  temporal    PP+NP+ADVP  arrive at noon 
7
-CLR  closely related   PP+NP+ADVP  work as a researcher 
6
-LOC  location    PP    live in Belgium 
4
-DIR  direction   PP walk towards the door
3
-EXT  extent   PP+NP drop 10 %
1
-PRP  purpose  PP+SBAR  die as a result of 
1
Anchor tags
Anchor tags describe how prepositional noun phrases (PNP) are attached to other chunks in the sentence. For example, in the sentence, I eat pizza with a fork, the anchor of with a fork is eat because it answers the question: "In what way do I eat?"

Tag   Description Example
A1 anchor chunks that corresponds to P1   eat with a fork
P1 PNP that corresponds to A1 eat with a fork

}}}
"""

"""
{{{ RELATIONS
IS-A 
PROPERTY-OF
PART-OF
CONTAINS

associated_with 
physically_related_to 
consists_of 
connected_to 
interconnects 
branch_of 
tributary_of 
ingredient_of 
spatially_related_to 
location_of 
adjacent_to 
surrounds 
traverses 
functionally_related_to 
affects 
manages 
treats 
disrupts 
complicates 
interacts_with 
prevents 
brings_about 
produces 
causes 
performs 
carries_out 
exhibits 
practices 
occurs_in 
process_of 
users 
manifestation_of 
indicates 
result_of 
temporally_related_to 
co-occurs_with 
precedes 
conceptually_related_to 
evaluation_of 
degree_of 
analyzes 
assesses_effect_of 
measurement_of 
measures 
diagnoses 
derivative_of 
developmental_form_of 
method_of 
conceptual_part_of 
issue_in 



   NOTA: 
      Para poder diferencias cosas como:
      - Juanita tiene brazos: PART-OF(brazos, juanita)
      - Juanita tiene coche: PROPERTY-OF(coche, juanita)
      Necesitamos un aprendizaje basico (basic facts) tipo:
      - Los brazos son parte del cuerpo humano
      - Los coches pueden ser propiedad de alguien


}}}
"""

import sys
import unicodedata
from pattern.search import match
from pattern.search import search
from pattern.search import Pattern
from pattern.es import parse
from pattern.es import parsetree
from pattern.es import conjugate, lemma, lexeme, tenses
from pattern.es import singularize, pluralize, attributive, MALE, SINGULAR
from random import randint


class nlp:
   
   # {{{ strip_accents() 
   def strip_accents(self, s):
      return ''.join(c for c in unicodedata.normalize('NFD', s)
         if unicodedata.category(c) != 'Mn')
   # }}}
  
   # {{{ get_quantifier_from_NN_JJ()
   def get_quantifier_from_NN_JJ(self, noun):
      if noun==singularize(noun):
         return "one"
      elif noun==pluralize(noun):
         return "all"
      else:
         print "ERROR: get_quantifier_from_NN_JJ():", noun, "!=", \
            singularize(noun), pluralize(noun)
         sys.exit(0)
   # }}}
    
   # {{{ get_quantifier_from_DT()
   def get_quantifier_from_DT(self, dt):  
      if dt.lower() in ["el", "la", "lo", "un", "uno", "una"]:
         return "one"
      elif dt.lower() in ["los", "las", "todos", "todas"]:
         return "all"
      elif dt.lower() in ["algun", "alguna", "algunos", "algunas", 
         "unos", "unas"]:
         return "exist"
      else:
         print "ERROR: parse_NP(): unknown DT '"+str(dt.lower())+"'"
         sys.exit(0)
   # }}}

   # {{{ get_quantifier_from_IN()
   def get_quantifier_from_IN(self, dt):  
      if dt.lower() in ["a"]:
         return "one"
      else:
         print "ERROR: parse_NP(): unknown DT '"+str(dt.lower())+"'"
         sys.exit(0)
   # }}}

   # {{{ parse_NP()
   def parse_NP(self, words):
      quantifier=""
      noun=""
      properties=[]

      # NNP
      if len(words)==1 and \
         words[0].tag[:3]=="NNP":
         noun = singularize(words[0].string)
         quantifier="one"
   
      # NN
      elif len(words)==1 and \
         (words[0].tag[:2]=="NN" or words[0].tag[:2]=="JJ"):
         noun = singularize(words[0].string)
         quantifier=self.get_quantifier_from_NN_JJ(words[0].string)
       
      # DT + NN
      elif len(words)==2 and \
           words[0].tag=="DT" and \
           words[1].tag[:2]=="NN":
         noun = singularize(words[1].string)
         quantifier=self.get_quantifier_from_DT(words[0].string)          

      # IN + NN
      elif len(words)==2 and \
           words[0].tag=="IN" and \
           words[1].tag[:2]=="NN":
         noun = singularize(words[1].string)
         quantifier=self.get_quantifier_from_IN(words[0].string)          

      # DT + JJ
      elif len(words)==2 and \
           words[0].tag=="DT" and \
           words[1].tag[:2]=="JJ":
         noun = singularize(words[1].string)
         quantifier=self.get_quantifier_from_DT(words[0].string)          

      # DT + NN + NN
      elif len(words)==3 and \
           words[0].tag=="DT" and \
           words[1].tag[:2]=="NN" and \
           words[2].tag[:2]=="NN":
         noun = singularize(words[1].string)
         quantifier=self.get_quantifier_from_DT(words[0].string)          
         # TODO: process composite nouns: NN+NN

      # DT + NN + JJ
      elif len(words)==3 and \
           words[0].tag=="DT" and \
           words[1].tag[:2]=="NN" and \
           words[2].tag[:2]=="JJ": 
         noun = singularize(words[1].string)
         quantifier=self.get_quantifier_from_DT(words[0].string)          
         # TODO: process JJ

      # DT + DT + NN
      elif len(words)==3 and \
           words[0].tag=="DT" and \
           words[1].tag=="DT" and \
           words[2].tag[:2]=="NN":
         noun = singularize(words[2].string)
         quantifier=self.get_quantifier_from_DT(words[0].string)

      # DT + NN + IN + NN
      elif len(words)==4 and \
           words[0].tag=="DT" and \
           words[1].tag[:2]=="NN" and \
           words[2].tag[:2]=="IN" and \
           words[3].tag[:2]=="NN":
         noun = singularize(words[1].string)
         quantifier=self.get_quantifier_from_DT(words[0].string)          
         # TODO: process composite nouns: NN+IN+NN


      else:
         print "ERROR: parse_NP(): not found!"
         print words
         sys.exit(0)

      return quantifier, noun, properties
   # }}}

   # {{{ relation_is_a()
   def relation_is_a(self, Aq, An, Aprop, Bq, Bn, Bprop):
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

   # {{{ relation_property_of()
   def relation_property_of(self, Aq, An, Aprop, Bq, Bn, Bprop):
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

   # {{{ relation_part_of()
   def relation_part_of(self, Aq, An, Aprop, Bq, Bn, Bprop):
      r=dict()
      r['code']=0
      r["type"]="relation"
      r["source_quantifier"]=Aq
      r["source"]=An
      r["destination_quantifier"]=Bq
      r["destination"]=Bn
      r["relation"]='PART-OF'
      return r
   # }}}

   # {{{ relation_contains()
   def relation_contains(self, Aq, An, Aprop, Bq, Bn, Bprop):
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

   # {{{ parse_sentence_greetings()
   def parse_sentence_greetings(self, t):
      greeting=t.string.strip()

      greeting_list_q=["hola", "buenas"]
      greeting_list_a=["hola", "buenas"]
      if self.strip_accents(greeting.lower()) in greeting_list_q:
         r=dict()
         r['code']=0
         r['type']='direct_answer'
         r['message']=greeting_list_a[randint(0,len(greeting_list_a)-1)]
         return [r]

      greeting_list_q=["que tal", "como estas", "como va",  
         "como te encuentras", "va todo bien"]
      greeting_list_a=["Estoy bien, gracias por preguntar"]
      if self.strip_accents(greeting.lower()) in greeting_list_q:
         r=dict()
         r['code']=0
         r['type']='direct_answer'
         r['message']=greeting_list_a[randint(0,len(greeting_list_a)-1)]
         return [r]

      greeting_list_q=["buenos dias", "buenas tardes", "buenas noches"]
      greeting_list_a=["hola", "buenas"]
      if self.strip_accents(greeting.lower()) in greeting_list_q:
         r=dict()
         r['code']=0
         r['type']='direct_answer'
         r['message']=greeting_list_a[randint(0,len(greeting_list_a)-1)]
         return [r]

      return None
   # }}}

   # {{{ parse_sentence_question()
   def parse_sentence_question(self, t):
      question=t.string[:-1].strip()
      question_list=["que es"]
      for q in question_list:
         if self.strip_accents(question.lower()).startswith(q):
            q, n, p = self.parse_NP(t.words[2:len(t.words)])
            r=dict()
            r['code']=0
            r['type']='query'
            r['relation']='IS-A'
            r['object']=n
            # TODO: process quantifier and properties
            return [r]

      return None
   # }}}

   # {{{ split_x_and_y()
   def split_x_and_y(self, t):
      x=[]
      y=[]
      found=0
      for w in t.words: 
         if w.string=="y":
            found=1  
            continue
         if found==0:
            x.append(w)
         else:
            y.append(w)

      return x, y
   # }}}

   # {{{ split_x_relation_y()
   def split_x_relation_y(self, t):
      x=[]
      y=[]
      found=0
      for w in t.words: 
         if w.tag=="VB":
            vp=lemma(w.string)
            found=1 
            continue
         if found==0:
            x.append(w)
         else:
            y.append(w)


      if vp=="ser":
         relation="IS-A"

         # es propiedad de
         if len(y)>2 and y[0].string=="propiedad" and y[1].string=="de":
            y=y[2:]
            relation="PROPERTY-OF"

         # es parte de
         if len(y)>2 and y[0].string=="parte" and y[1].string=="de":
            y=y[2:]
            relation="PART-OF"

      if vp=="contener":
         relation="CONTAINS"


      return x, relation, y
   # }}}

   # {{{ parse_sentence_x_VB_y()
   def parse_sentence_x_VB_y(self, t):
      n_vb=0

      # Count number of verbs
      for w in t.words: 
         if w.tag=="VB":
            n_vb+=1

      # Only one verb
      if n_vb==1:
         x, relation, y = self.split_x_relation_y(t)
         npA_q, npA_n, npA_prop = self.parse_NP(x)
         npB_q, npB_n, npB_prop = self.parse_NP(y)

         if relation=="IS-A":
            return [self.relation_is_a(npA_q, npA_n, npA_prop, 
                                       npB_q, npB_n, npB_prop)]

         elif relation=="PROPERTY-OF":
            return [self.relation_property_of(npA_q, npA_n, npA_prop, 
                                              npB_q, npB_n, npB_prop)]

         elif relation=="PART-OF":
            return [self.relation_part_of(npA_q, npA_n, npA_prop, 
                                          npB_q, npB_n, npB_prop)]

         elif relation=="CONTAINS":
            return [self.relation_contains(npA_q, npA_n, npA_prop, 
                                           npB_q, npB_n, npB_prop)]


      return None
   # }}}

   # {{{ sentence_pre_processing()
   def sentence_pre_processing(self, sentence):
      sentence=sentence.replace(' del ', ' de el ')

      # Use less ambiguous forms
      # PROPERTY-OF
      sentence=sentence.replace(' es de ', ' es propiedad de ')
      sentence=sentence.replace(' pertenece a ', ' es propiedad de ')
      # PART-OF
      sentence=sentence.replace(' forma parte de ', ' es parte de ')
      sentence=sentence.replace(' forman parte de ', ' son parte de ')
      # CONTAINS
      sentence=sentence.replace(' tiene dentro ', ' contiene ')



      if sentence[-1:]=='.':
         sentence = sentence[:-1]
      return sentence
   # }}}

   # {{{ parse_sentence()
   def parse_sentence(self, sentence):
      sentence=self.sentence_pre_processing(sentence)
      t = parsetree(sentence, lemmata=True)

      r=self.parse_sentence_greetings(t)
      if r!=None: 
         return r

      r=self.parse_sentence_question(t)
      if r!=None: 
         return r

      r=self.parse_sentence_x_VB_y(t)
      if r!=None: 
         return r

      r=dict()
      r["code"]="-1"
      r["error_description"]="ERROR: parse_sentence(), sentence:"+sentence

      return [r]
   # }}}


if __name__ == "__main__":
   nl=nlp()
   print nl.parse_sentence('El mosquito es un insecto.');
   print nl.parse_sentence('Los mosquitos son insectos.');
   print nl.parse_sentence('Todos los mosquitos son insectos.');
   print nl.parse_sentence('Un mosquito es un insecto.');
   print nl.parse_sentence('El mosquito es un insecto.');
   print nl.parse_sentence('El coral es animal.');
   print nl.parse_sentence('La espátula común es un animal.');
   print nl.parse_sentence('El insecto palo es un animal.');
   print nl.parse_sentence('El caballito de mar es un animal.');

   print nl.parse_sentence('El perro es propiedad de Juan.');
   print nl.parse_sentence('El perro pertenece a Juan.');
   print nl.parse_sentence('El perro es de Juan.');

   print nl.parse_sentence('Los brazos son parte del cuerpo humano.');
   print nl.parse_sentence('Las piernas son parte del cuerpo humano.');
   print nl.parse_sentence('Los ojos forman parte del cuerpo humano.');

   print nl.parse_sentence('La caja tiene dentro unos libros.');




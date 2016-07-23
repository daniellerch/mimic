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

Tag    Description + Example
==============================================================================
CC     conjunction, coordinating  and, or, but
CD     cardinal number    five, three, 13%
DT     determiner  the, a, these 
EX     existential there there were six boys 
FW     foreign word    mais 
IN     conjunction, subordinating or preposition of, on, before, unless 
JJ     adjective    nice, easy
JJR    adjective, comparative  nicer, easier
JJS    adjective, superlative  nicest, easiest 
LS     list item marker    
MD     verb, modal auxillary    may, should 
NN     noun, singular or mass  tiger, chair, laughter 
NNS    noun, plural    tigers, chairs, insects 
NNP    noun, proper singular    Germany, God, Alice 
NNPS  noun, proper plural  we met two Christmases ago 
PDT    predeterminer  both his children 
POS    possessive ending 's
PRP    pronoun, personal me, you, it 
PRP$  pronoun, possessive  my, your, our 
RB     adverb    extremely, loudly, hard  
RBR    adverb, comparative  better 
RBS    adverb, superlative  best 
RP     adverb, particle  about, off, up 
SYM    symbol    % 
TO     infinitival to what to do? 
UH     interjection    oh, oops, gosh 
VB     verb, base form    think 
VBZ    verb, 3rd person singular present    she thinks 
VBP    verb, non-3rd person singular present  I think 
VBD    verb, past tense  they thought 
VBN    verb, past participle    a sunken ship 
VBG    verb, gerund or present participle  thinking is fun 
WDT    wh-determiner  which, whatever, whichever 
WP     wh-pronoun, personal what, who, whom 
WP$    wh-pronoun, possessive  whose, whosever 
WRB    wh-adverb    where, when 
.      punctuation mark, sentence closer    .;?* 
,      punctuation mark, comma , 
:      punctuation mark, colon : 
(      contextual separator, left paren ( 
)      contextual separator, right paren    ) 


Chunk tags
^^^^^^^^^^
Chunk tags are assigned to groups of words that belong together (i.e. phrases).
The most common phrases are the noun phrase (NP, for example the black cat) 
and the verb phrase (VP, for example is purring).

Tag    Description                     Words                     Example
==============================================================================
NP     noun phrase                     DT+RB+JJ+NN + PR      the strange bird
PP     prepositional phrase         TO+IN                     in between
VP     verb phrase                     RB+MD+VB                 was looking
ADVP  adverb phrase                  RB                         also
ADJP  adjective phrase              CC+RB+JJ                 warm and cosy
SBAR  subordinating conjunction  IN                         whether or not
PRT    particle                         RP                         up the stairs
INTJ  interjection                    UH                         hello

The IOB prefix marks whether a word is inside or outside of a chunk.


Tag    Description
==============================================================================
I-     inside the chunk
B-     inside the chunk, preceding word is part of a different chunk
O      not part of a chunk

A prepositional noun phrase (PNP) is a group of chunks starting with a 
preposition (PP) followed by noun phrases (NP), for example: under the table.

Tag    Description Chunks    Example
PNP    prepositional noun phrase  PP+NP as of today
Relation tags

Relations tags describe the relation between different chunks, and clarify the role of a chunk in that relation. The most common roles in a sentence are SBJ (subject noun phrase) and OBJ (object noun phrase). They link NP to VP chunks. The subject of a sentence is the person, thing, place or idea that is doing or being something. The object of a sentence is the person/thing affected by the action.

Tag    Description             Chunks        Example                                  %
-SBJ  sentence subject      NP             the cat sat on the mat              35
-OBJ  sentence object        NP+SBAR      the cat grabs the fish              27
-PRD  predicate                PP+NP+ADJP  the cat feels warm and fuzzy      7
-TMP  temporal                 PP+NP+ADVP  arrive at noon                         7
-CLR  closely related        PP+NP+ADVP  work as a researcher                 6
-LOC  location                 PP             live in Belgium                        4
-DIR  direction                PP             walk towards the door                3
-EXT  extent                    PP+NP         drop 10 %                                1
-PRP  purpose                  PP+SBAR      die as a result of                    1
Anchor tags
Anchor tags describe how prepositional noun phrases (PNP) are attached to other chunks in the sentence. For example, in the sentence, I eat pizza with a fork, the anchor of with a fork is eat because it answers the question: "In what way do I eat?"

Tag    Description Example
A1 anchor chunks that corresponds to P1    eat with a fork
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
from pattern.es import singularize, pluralize, attributive, SINGULAR, PLURAL
from pattern.es import MALE, FEMALE
from random import randint
from pattern.text.tree import Text

from knowledge.base import Concept


# {{{ pattern_match()
def pattern_match(pattern, sentence):

    if type(sentence) is not Text:
        sentence = parsetree(sentence, lemmata=True)

    p = Pattern.fromstring(pattern)
    try:
        m = p.match(sentence)
        return m
    except:
        return None
# }}}

# {{{ learn_gender()
def learn_gender(dt, noun):
    
    male_words=["el", "un", "uno", "unos", "los", "todos", "algunos", "algun"]
    female_words=["la", "una", "unas", "las", "todas", "algunas", "alguna"]

    
    concept=Concept(noun)

    if dt in female_words:
        concept.set_gender('f')
    else:
        concept.set_gender('m')
        
    return

# }}}

# {{{ Word_list_to_Text()
def Word_list_to_Text(Word_list):
    string=''
    for w in Word_list:
        string+=w.string+' '
    
    return parsetree(string)
# }}}

# {{{ get_quantifier_from_NN_JJ()
def get_quantifier_from_NN_JJ(noun):
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
def get_quantifier_from_DT(dt):  
    if dt.lower() in ["el", "la", "lo", "un", "uno", "una"]:
        return "one"
    elif dt.lower() in ["los", "las", "todos", "todas"]:
        return "all"
    elif dt.lower() in ["algun", "alguna", "algunos", "algunas", 
        "unos", "unas"]:
        return "exist"
    else:
        print "ERROR: get_quantifier_from_DT(): unknown DT '"+str(dt.lower())+"'"
        sys.exit(0)
# }}}

# {{{ get_quantifier_from_IN()
def get_quantifier_from_IN(dt):  
    if dt.lower() in ["a"]:
        return "one"
    else:
        print "ERROR: get_quantifier_from_IN(): unknown DT '"+str(dt.lower())+"'"
        sys.exit(0)
# }}}

# {{{ parse_NP()
def parse_NP(words):
    quantifier=""
    noun=""
    properties=[]
    gender='m'

    t=Word_list_to_Text(words)

    
    #NP     noun phrase     DT+RB+JJ+NN + PR      the strange bird


    # Example: todos los perros
    m=pattern_match("{DT} {DT} {JJ*|NN*}", t)
    if m and len(m)==len(t.words):
        noun = singularize(m.group(3)[0].string)
        quantifier=get_quantifier_from_DT(m.group(1)[0].string)
        learn_gender(m.group(2)[0].string, noun)
        return quantifier, gender, noun, properties

    # Example: el perro
    m=pattern_match("{DT} {JJ*|NN*}", t)
    if m and len(m)==len(t.words):
        noun = singularize(m.group(2)[0].string)
        quantifier=get_quantifier_from_DT(m.group(1)[0].string)
        learn_gender(m.group(1)[0].string, noun)
        return quantifier, gender, noun, properties

    # Example: verde
    m=pattern_match("{JJ*|NN*}", t)
    if m and len(m)==len(t.words):
        noun=m.group(1)[0].string
        quantifier="one"
        if noun==pluralize(noun):
            quantifier="all"
        noun = singularize(noun)
     
        return quantifier, gender, noun, properties

    print "parse_NP() : not found", t
    sys.exit(0)


    """
    # NNP
    if len(words)==1 and \
        words[0].tag[:3]=="NNP":
        noun = singularize(words[0].string)
        quantifier="one"

    # NN
    elif len(words)==1 and \
        (words[0].tag[:2]=="NN" or words[0].tag[:2]=="JJ"):
        noun = singularize(words[0].string)
        quantifier=get_quantifier_from_NN_JJ(words[0].string)
     
    # DT + NN
    elif len(words)==2 and \
          words[0].tag=="DT" and \
          words[1].tag[:2]=="NN":
        noun = singularize(words[1].string)
        quantifier=get_quantifier_from_DT(words[0].string)             

    # IN + NN
    elif len(words)==2 and \
          words[0].tag=="IN" and \
          words[1].tag[:2]=="NN":
        noun = singularize(words[1].string)
        quantifier=get_quantifier_from_IN(words[0].string)             

    # DT + JJ
    elif len(words)==2 and \
          words[0].tag=="DT" and \
          words[1].tag[:2]=="JJ":
        noun = singularize(words[1].string)
        quantifier=get_quantifier_from_DT(words[0].string)             

    # DT + NN + NN
    elif len(words)==3 and \
          words[0].tag=="DT" and \
          words[1].tag[:2]=="NN" and \
          words[2].tag[:2]=="NN":
        noun = singularize(words[1].string)
        quantifier=get_quantifier_from_DT(words[0].string)             
        # TODO: process composite nouns: NN+NN

    # DT + NN + JJ
    elif len(words)==3 and \
          words[0].tag=="DT" and \
          words[1].tag[:2]=="NN" and \
          words[2].tag[:2]=="JJ": 
        noun = singularize(words[1].string)
        quantifier=get_quantifier_from_DT(words[0].string)             
        # TODO: process JJ

    # DT + DT + NN
    elif len(words)==3 and \
          words[0].tag=="DT" and \
          words[1].tag=="DT" and \
          words[2].tag[:2]=="NN":
        noun = singularize(words[2].string)
        quantifier=get_quantifier_from_DT(words[0].string)

    # DT + NN + IN + NN
    elif len(words)==4 and \
          words[0].tag=="DT" and \
          words[1].tag[:2]=="NN" and \
          words[2].tag[:2]=="IN" and \
          words[3].tag[:2]=="NN":
        noun = singularize(words[1].string)
        quantifier=get_quantifier_from_DT(words[0].string)             
        # TODO: process composite nouns: NN+IN+NN


    else:
        print "ERROR: parse_NP(): not found!"
        print words
        sys.exit(0)
    """

    return quantifier, noun, properties
# }}}

# {{{ sentence_pre_processing()
def sentence_pre_processing(sentence):

    # TODO:
    # - Preprocess personal names juan->Juan 

    # Easy tagging
    sentence=sentence.replace(' del ', ' de el ')



    if sentence[-1:]=='.':
        sentence = sentence[:-1]
    return sentence
# }}}



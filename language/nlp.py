#!/usr/bin/python
# -*- coding: utf-8 -*-

from pattern.es import parsetree
import language.es.structures as structures
import language.es.greetings as greetings
import language.es.questions as questions
import language.es.relations as relations

class nlp:

   # {{{ parse_sentence()
   def parse_sentence(self, sentence):

      sentence=sentence.lower()
      sentence=structures.sentence_pre_processing(sentence)

      t = parsetree(sentence, lemmata=True)
    
      r=greetings.process(t)
      if r: return r

      r=questions.process(t)
      if r: return r

      r=relations.process(t)
      if r: return r

      r=dict()
      r["code"]="-1"
      r["error_message"]="No te he entendido. ¿Podrías reformular la frase?"

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




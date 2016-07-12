#!/usr/bin/python

import sys
from language.chatbot import chatbot

if __name__ == '__main__':

   cb=chatbot()

   while True: 
      try:
         human_input=raw_input("mimic #> ")
         #.decode("utf-8")
         if len(human_input)==0:
            continue

         if human_input=="exit" or human_input=="quit" or human_input=="q":
            sys.exit(0)
         
         print cb.talk(human_input)

      except KeyboardInterrupt:
         print
         sys.exit(0)
         





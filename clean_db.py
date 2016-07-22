#!/usr/bin/python

import sys
import glob
from manager.chatbot import chatbot

if __name__ == '__main__':

    cb=chatbot()
    cb.clean_memory()


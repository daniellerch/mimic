#!/usr/bin/python
# -*- coding: utf-8 -*-


definite_articles=["el", "la", "los", "las"]
indefinite_articles=["un", "uno", "una", "unos", "unas"]

is_a=["es", "son"]


# {{{ to_singular()
def to_singular(w):

   w = w.lower()

   if w.endswith("es") and w[:-2].endswith(("br", "i", "j", "t", "zn")):
      return w[:-1]

   for s, p in ( ("anes", u"án"), ("enes", u"én"), ("eses", u"és"),
                 ("ines", u"ín"), ("ones", u"ón"), ("unes", u"ún") ):
      if w.endswith(s):
         return w[:-4] + p

   if w.endswith(("esis", "isis", "osis")):
      return w

   if w.endswith("ces"):
      return w[:-3] + "z"

   if w.endswith("es"):
      return w[:-2]

   if w.endswith("s"):
      return w[:-1]

   return w
# }}}

# {{{ to_plural()
def to_plural(w):

   w = w.lower()

   for a, b in ( (u"mamá", u"mamás"), (u"papá", u"papás"),
                 (u"sofá", u"sofás") , (u"dominó", u"dominós") ):
      if w==a:
         return b


   if w.endswith( ("idad", "esis", "isis", "osis", "dica", u"grafía", u"logía") ):
      return w

   if w.endswith( ("a", "e", "i", "o", "u") ) or w.endswith(u"é"):
      return w + "s"

   if w.endswith((u"á", u"é", u"í", u"ó", u"ú")):
      return w + "es"

   if w.endswith(u"és"):
      return w[:-2] + "eses"

   if w.endswith(u"s") and len(w) > 3 and is_vowel(w[-2]):
      return w

   if w.endswith(u"z"):
      return w[:-1] + "ces"

   for a, b in ( (u"án", "anes"), (u"én", "enes"), (u"ín", "ines"),
                 (u"ón", "ones"), (u"ún", "unes") ):
      if w.endswith(a):
         return w[:-2] + b

   return w + "es"
# }}}




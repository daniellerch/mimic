#!/usr/bin/python
# -*- coding: utf-8 -*-

from pattern.search import Pattern
from pattern.es import parsetree

t = parsetree('Pedro es mas feo que Juan.', lemmata=True)
t = parsetree('Pedro fue mas alto que Juan.', lemmata=True)

p = Pattern.fromstring('{NP} ser mas {JJ} que {NP}')
m = p.match(t)
print m.group(1)
print m.group(2)
print m.group(3)

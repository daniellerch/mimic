from logic import *


fol = FOLEngine([
   expr('Farmer(Mac)'), 
   expr('Rabbit(Pete)'),
   expr('(Rabbit(r) & Farmer(f)) ==> Hates(f, r)')
])

fol.tell(expr('Rabbit(Flopsie)'))
fol.retract(expr('Rabbit(Pete)'))

print fol.ask(expr('Hates(Mac, x)'))
print fol.ask(expr('Wife(Pete, x)'))



fol = FOLEngine()

fol.tell(expr('Hombre(x) ==> Mortal(x)'))
fol.tell(expr('Griego(x) ==> Hombre(x)'))
fol.tell(expr('Hombre(Eratostenes)'))
fol.tell(expr('Hombre(Socrates)'))
fol.tell(expr('Hombre(Platon)'))

print fol.ask(expr('Griego(x)'))
print fol.ask(expr('Mortal(x)'))
print fol.ask(expr('Hombre(x)'))
print fol.ask(expr('Hombre(Platon)'))




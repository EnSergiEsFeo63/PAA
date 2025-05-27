#Extensió 1: Transformar GRAMATICA
#CFG (gram ind del context) --> CNF (forma normal de Chomsky)

"""
Teoria:
CFG: conjuny regles definieix com generar cadenes d'strings
clausules: G=(V, E, R, S)
V: conj finit varibles (no terminals) [S,A,B..]
E: alfabets de simbols (terminals) [a,b,c,..]
R: conj regles de producció [A-->aB]
S: start symbol (variable inicial, des de on comença derivació)

CNF: forma normal de Chomsky (versió estandard de CFG, regles més restrictives)
100% tenir una d'aquestes formes:
1. A --> BC (BC 2 vars no terminals)
2. A --> a (un terminal)
3. S --> ε (start symbol pot derivar a cadena buida, opcional)
[opció 3: unicament si cadena buida és part del llenguatge generat]

*ε= produccions buides (cadena buida)

Pasos a seguir per transformar una gramàtica CFG a CNF:
Totes clàusules han de complir una de les formes CNF.

EXPLICACIÓ WHATAPP SILVIA LINK


VALE EN CADA VIDEO VEIG UNES REGLES DIFERENTS :(((((((((((

0. New productions:

1. Add ε-productions (si cadena buida és part del llenguatge)




1. Eliminar start symbol per un right-hand side ()



"""

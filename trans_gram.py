#Extensió 1: Transformar GRAMATICA
#CFG (gram ind del context) --> CNF (forma normal de Chomsky)
 
import copy

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


class GramTrans_CFGtoCNF:
    def __init__(self, gram_original):
        """
        gram_original: gram CFG a transformar (list)
        """
        self.gram_org = gram_original #gram original (argument de la instancia)
        #primer simbol:
        self.start= next(iter(gram_original.keys())) #primer simbol no terminal (start symbol)
        #no terminals:
        self.no_term= set(gram_original.keys())
        #termiansl:
        self.term= {t for rhss in gram_original.values() for rhs in rhss for t in rhs if self._es_terminal(t)}
        
        self.P = copy.deepcopy(gram_original) # copia profunda original --> no modifica estructura original gram_org 
        #Nous simbols 
        self.contador = 0 #comptador per generar nous
        self.S0= self._new_no_term('S0') 




    def _es_terminal(self, simbol):
        """
        True si simbol no és no_terminal ni cadena buida (ε).
        """
        return not (simbol in self.no_term or simbol == 'ε')

    def _new_no_term(self, prefix:str):
        """
        Genera nou simbol no terminal únic basat en un prefix donat.
        """
        while True:
            self.contador += 1
            nou_no_term = f"{prefix}{self.contador}"
            if nou_no_term not in self.no_term: #incloure en no_term (si no existeix previament)
                self.no_term.add(nou_no_term)
                return nou_no_term

    ###########
    #metodes privats 
    ###########
    def _add_start_symbol(self):
        #afegrir un nou start symbol S0
        self.P[self.S0] = [[self.start]]  # afegir gram original com a producció de S0
        

    def _remove_epsilon_productions(self):
        """
        elimina produccions buides (ε-productions) en termes P.
        """
        # 1) Trobar epsilon-produccions --> sempre representades com 'ε' en les regles de producció, no com list buide []
        epsilon_productions = {nt for nt, rhss in self.P.items() if any(rhs == ['ε'] for rhs in rhss)}
        change = True
        while change:
            change = False
            for A, rhss in self.P.items():
                for rhs in rhss:
                    if all(X in epsilon_productions for X in rhs) and A not in epsilon_productions:
                        epsilon_productions.add(A)
                        change = True
        # Ara epsilon_productions conté les variables que poden derivar a ε
        
        # 2) Reescriure produccions (eliminar ε-produccions)
        from itertools import chain, combinations
        new_P = {}

        for A, rhss in self.P.items():
            new_rhss = []
            for rhs in rhss:
                #index simbol epsilon-productions en rhs
                null_pos= [i for i, X in enumerate(rhs) if X in epsilon_productions]
                #Si no hiha simbols nullables --> conservar regla original
                if not null_pos:
                    if rhs not in new_rhss:
                        new_rhss.append(list(rhs))
                        continue
                #Si hi ha nullables, generar noves produccions (sense els nullables)
                for remove in chain.from_iterable(combinations(null_pos, r) for r in range(len(null_pos) + 1)):
                    if set(remove)== set(null_pos) and A!=self.S0:
                        continue
                    new_rhs = [X for i, X in enumerate(rhs) if i not in remove]
                    if not new_rhs: #si queda buida representem com ε
                        new_rhs = ['ε']
                    if new_rhs not in new_rhss:
                        new_rhss.append(new_rhs) #evitar duplicats
                    
            # Save totes produccions no buides (ε-productions)
            # menys si A es S0 --> el nou inici pot derivar a ε
            new_P[A]=[rhs for rhs in new_rhss if rhs != ['ε'] or A == self.S0]

        self.P = new_P


    def _remove_unit_productions(self): #despres d'aplicar --> no queden regles on RHS sigui un sol no terminal
        """
        Elimina unit productions (produccions unitàries) de la gramàtica.
        A--> B (on A i B són no terminals).
        """
        # 1) Conj parells unitaris directes
        unit_pairs= {
            #recorrer cada no terminal A i les seves produccions 
            (A, rhs[0]) 
            for A, rhss in self.P.items() 
            for rhs in rhss 
            if len(rhs) == 1 and rhs[0] in self.no_term #si la llista RHS es un sol terme (inclos en no_terminals)
            }                                           #Incloure en unit_pairs        }

        # 2) Busquem cadenes unitaries transitives i tanquem
        #si A → B i B → C, llavors A → C també és una unit production
        unit_pairs= set() 

        for A in self.no_term: 
            visited = set()
            stack = [A]
            while stack:
                X = stack.pop()
                for rhs in self.P.get(X, []):
                    if len(rhs) == 1 and rhs[0] in self.no_term:
                        B = rhs[0]
                        if B not in visited:
                            visited.add(B)
                            unit_pairs.add((A, B))
                            stack.append(B)

        print('Unit pairs:', unit_pairs)
        # 3) Nova taula de produccions (treure unit productions)
        new_P = { #Copiar no unitaries
            A: [rhs for rhs in rhss #filtrar unicament no siguin unitaris
                if not (len(rhs) == 1 and rhs[0] in self.no_term) #eliminar unit productions
                ]
            for A, rhss in self.P.items()
        }
        # 4) Afegir produccions transitives
        print('New_p ANTES TRANSFER:',new_P['S01'])
        for (A,B) in unit_pairs:
            for rhs in self.P.get(B, []):
                if not (len(rhs) == 1 and rhs[0] in self.no_term):
                    if rhs not in new_P[A]:
                        new_P[A].append(rhs)
        print('New_p DESPUES TRANSFER:',new_P['S01'])
        # 5) Actualitzar P 
        self.P = new_P                


    #FALTAAAAAA --> TE PROBLEMESSS ;((
    def _remove_long_right_hand_sides(self):
        """
        Fragmentar les regles llargues A-> B1 B2 ... Bn
        on n > 2, en regles més curtes A -> B1 C1, C1 -> B2 C2, ..., Cn-1 -> Bn.
        """
        term={}
        new_P = {}

        for A, rhss in self.P.items():
            print(f'Procesar {A}--> {rhss}')
            new_rhss = []

            for rhs in rhss:
                print(f'  Analizar RHS: {rhs}')
                #1) Substituir termianls si RHS té més de 1 simbol

                if len(rhs) > 1 :
                    rhs2=[]

                    for X in rhs:
                        if self._es_terminal(X):
                            T=term.get(X) 
                            if not T:           # o crea nou terminal
                                T= self._new_no_term(f'T_{X}')
                                term[X] = T
                                #afeguir la regla T-> X
                                new_P.setdefault(T, []).append([X])
                                print(f'Creat {T}--> {X}')

                            rhs2.append(T)
                            print(f"    → Substitució terminal: {X} → {T}")
                            
                        else:
                            rhs2.append(X)
                    
                    print(f'Despres substitució: {rhs2}')
                
                else: #es sols un terminal 
                    rhs2= rhs.copy() 
                    print(f"    → RHS de longitud 1, sin sustituciones: {rhs2}")

                #2) Si té més de 2 símbols, FRAGMENTACIÓ en regles binaries
                if len(rhs2) <=2:
                    new_rhss.append(rhs2)
                else:
                    # Fragmentar en regles binàries
                    prev= rhs2[0]  
                    for i in range(1, len(rhs2) - 1):
                        next_no_term = self._new_no_term('Z')
                        new_rhss.append([prev, next_no_term])  # A -> B1 C1
                        
                        print(f"    → Fragmentació: {prev} → {next_no_term}")
                        
                        prev = next_no_term  # Actualitzar prev per la següent iteració
                    
                    new_rhss.append([prev, rhs2[-1]])   
                    print(f'fragmentacio {prev} → {rhs2[-1]}')
                
            new_P[A] = new_rhss  # Afegir regles noves a la gramàtica
        
        ####Acabar bucle principal####    
        self.P = new_P  # Actualitzar la gramàtica amb les noves regles

    def to_cnf(self):
        """
        Transforma gramàtica CFG a CNF.
        Retorna gramàtica en CNF.
        """
        self._add_start_symbol()
        self._remove_epsilon_productions()
        self._remove_unit_productions()
        self._remove_long_right_hand_sides()
        return self.P







####################################################################################
#PROVAR
# Gramática de ejemplo
G = {
    'S': [['A','B'], ['b']],
    'A': [['a'], ['ε']],   # A → ε
    'B': [['b'], ['ε']],   # B → ε
}

t= GramTrans_CFGtoCNF(G)
t._add_start_symbol()
print('Antes', t.P)
t._remove_epsilon_productions()
print('Después', t.P)

print()
print('-----------------------------------')
print()


F= {
  'S': [['A'], ['b']],
  'A': [['B']],
  'B': [['c']]
}
t = GramTrans_CFGtoCNF(F)
t._add_start_symbol()
print('Antes', t.P)
t._remove_epsilon_productions()
print('Después', t.P)
t._remove_unit_productions()
print('Después de eliminar unit productions', t.P)


H = {
      'S': [['A', 'b', 'C', 'D']], 
      'A': [['a']], 'C': [['c']], 
      'D': [['d']]
      }

t = GramTrans_CFGtoCNF(H)
t._add_start_symbol()
print('Antes', t.P)
t._remove_epsilon_productions()
print('Después', t.P)
t._remove_unit_productions()
print('Después de eliminar unit productions', t.P)

print()
print()
t._remove_long_right_hand_sides() #correcte 
print('Después de eliminar long right hand sides', t.P)


#####################
#PASOS FALTANTS:
#1, UNIR AMB CODI SAM
#2, CREAR JOCS PROVES MILLORS
#####################
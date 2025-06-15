#Extensió 1: Transformar GRAMATICA
#CFG (gram ind del context) --> CNF (forma normal de Chomsky)
 
import copy

class GramTrans_CFGtoCNF:
    def __init__(self, gram):
        self.original= copy.deepcopy(gram)
        self.grammar= copy.deepcopy(gram)
        self.new_var_count = 0 # comptador per generar nous no terminals únics
        self.start_sym= next(iter(gram))


    def _nova_var(self):
        self.new_var_count += 1
        return f'X{self.new_var_count}'
    
    def es_cnf(self):
        for lhs, rhss in self.grammar.items():
            for rhs in rhss:
                #simbol inicial pot tenir produccio buida
                if rhs ==[]:
                    if lhs != self.start_sym:
                        return False
                    continue
                #Produccions de un sol simbol --> ha de ser 100% terminal (minuscula)
                if len(rhs) == 1:
                    if rhs[0].isupper():
                        return False 
                # Per producciones binaries (A → BC) --> dos simbols han de ser NO termianls (mayuscules)
                elif len(rhs) == 2:
                    if not all(sym.isupper() for sym in rhs):
                        return False 
                else: #la resta tampoc es valid
                    return False
        return True


    #PAS1: Eliminar NULLS (epsilon-produccions--> categoritzat com a @empty)
     
    def eliminar_epsilon(self):
        s= set()
        # Trobar les produccions epsilon
        for lhs, rhss in self.grammar.items():
            for rhs in rhss:
                if rhs == ['ε'] or rhs == ['??'] or rhs == ['@empty'] or rhs == []:
                    s.add(lhs)
        changed = True
        while changed:
            changed = False
            for lhs, rhss in self.grammar.items():
                for rhs in rhss:
                    if any(sym in s for sym in rhs) and lhs not in s:
                        s.add(lhs)
                        changed = True
        #noves produccions (sense simbols null)
        new_grammar = {}
        for lhs, rhss in self.grammar.items():
            new_rhss = set()
            for rhs in rhss:
                #incloure original
                new_rhss.add(tuple(rhs)) 
                n_pos= [i for i, sym in enumerate(rhs) if sym in s]
                
                from itertools import combinations,chain
                for r in range(1, len(n_pos) +1):
                    for to_remove in combinations(n_pos, r):
                        new_rhs=[sym for i, sym in enumerate(rhs) if i not in to_remove]
                        if new_rhs:
                            new_rhss.add(tuple(new_rhs))
            new_grammar[lhs]= [list(rhs) for rhs in new_rhss ]
        
        self.grammar = new_grammar

    def ajustar_inicial_epsilon(self): #aplicar si es pot derivar indirectament epsilon de sim inicial
        def pot_ind_fer_epsilon(nt,vist=set()):
            #funcio auxiliar per comprovar si no-term pot derivar epsilon
            if nt in vist:
                return False
            vist.add(nt)
            for rhs in self.grammar.get(nt, []):
                if rhs == []:
                    return True
                if all(sym in self.grammar and pot_ind_fer_epsilon(sym, vist.copy()) for sym in rhs):
                    return True
            return False
        
        if pot_ind_fer_epsilon(self.start_sym):
            # Mirar sim inicial: si es pot afeguir S -> []
            if [] not in self.grammar[self.start_sym]:
                self.grammar[self.start_sym].append([])

        #eliminar les buides no permeses (la resta no-term que no son S)
        no_term= list(self.grammar.keys())
        for nt in no_term:
            if nt !=self.start_sym: #si conte buides i no es inicial --> eliminar
                self.grammar[nt] = [rhs for rhs in self.grammar[nt] if rhs != []]
                if not self.grammar[nt]:  
                    del self.grammar[nt]  #si queda buit --> eliminar

    
    #PAS2: Eiminar unitàries
    def eliminar_unitaries(self):
        #eliminar unitaries ja no existeixen --> es poden haver eliminat amb ajustar_inicial_epsilon
        for lhs in self.grammar:
            self.grammar[lhs] = [
                rhs for rhs in self.grammar[lhs]
                if not (len(rhs) == 1 and rhs[0].isupper() and rhs[0] not in self.grammar)
                                          #no eliminar las no terminals (minuscules)
            ]
                                
        unit_p=set()
        # Trobar les produccions unitàries
        for A in self.grammar:
            for rhs in self.grammar[A]:
                if len(rhs) == 1 and rhs[0] in self.grammar:
                    unit_p.add((A, rhs[0])) #trobar unitaries (A -> B)
        # tractar:
        changed = True
        while changed:
            changed = False
            noves_p= set(unit_p)
            for (A,B) in unit_p:
                for (C,D) in unit_p:
                    if B == C and (A, D) not in unit_p:
                        noves_p.add((A, D))
                        changed = True
            unit_p = noves_p

        #nova gram --> sense unitaries
        new_grammar = {}
        for A in self.grammar:
            new_grammar[A] = []
            for rhs in self.grammar[A]:
                if not (len(rhs) == 1 and rhs[0] in self.grammar):
                    new_grammar[A].append(rhs)

        #afegir unitaries
        for (A,B) in unit_p:
            for rhs in self.grammar[B]:
                if not (len(rhs)== 1 and rhs[0] in self.grammar):
                    if rhs not in new_grammar[A]:
                        new_grammar[A].append(rhs)

        self.grammar = new_grammar

    #PAS3: Convertir terminals
    #tractar produccions mixtes entre terminals i no-terminals (A->aB, A->a)
    def convertir_mixtes(self):
        terminal_map = {} #substituits
        new_rules = {} #noves regles [com a Xn]
        for lhs, rhss in self.grammar.items():
            new_rhss = []
            for rhs in rhss:
                if len(rhs) > 1:
                    #com té més d'un simbol -> mirar si son terminals no aptes
                    new_rhs = []
                    for sym in rhs:
                        if sym not in self.grammar and not sym.isupper():#mirar si es terminal(minuscules)
                            if sym not in terminal_map:
                                var = self._nova_var()
                                terminal_map[sym] = var
                                new_rules[var] = [[sym]]
                            new_rhs.append(terminal_map[sym])
                        else:
                            new_rhs.append(sym)
                    new_rhss.append(new_rhs)
                else:
                    new_rhss.append(rhs)
            self.grammar[lhs] = new_rhss

        self.grammar.update(new_rules) #actualitzar gram amb les noves regles

    #PAS4: Trencar regles llargues (Unicament permes regles BI no terminals)
    def trencar_regles_no_bi(self):
        new_rules = {} #guardar noves regles
        for lhs, rhss in self.grammar.items():
            new_rhss = []
            for rhs in rhss:
                while len(rhs) > 2: #trencat si més de 2 simbols
                    new_var = self._nova_var() #es crea un bi amb els dos ultims simbols
                    new_rules[new_var] = [[rhs[1], rhs[2]]]
                    rhs = [rhs[0], new_var] + rhs[3:] 
                    #continua si encara no son totes bi
                new_rhss.append(rhs)
            self.grammar[lhs] = new_rhss #substituir 
        self.grammar.update(new_rules) #actualitzar gram amb les noves regles


#REVISAT
    def to_cnf(self):
        if self.es_cnf():
            print("La gramàtica ja està en CNF.")
            return self.grammar
        print("Transformant la gramàtica a CNF...")

        #APLICAR TRANSFORMACIÓ
        # 0. convertir cada producció de string a LLISTA de símbols
        #[algoritme i transformació s'han plantejat diferent i cal transformar el format]
        
        for lhs in self.grammar:
            noves_produccions = []
            #tractar produccio buida epsilon --> @empty
            for rhs in self.grammar[lhs]:
                if rhs == '@empty':
                    noves_produccions.append([])  # representa epsilon internament
                else:
                    noves_produccions.append(list(rhs))
            self.grammar[lhs] = noves_produccions
        
        #1. Aplicar les transformacions necessàries
        #A. Tractar produccions buides (epsilon-produccions)
        self.eliminar_epsilon()
        #afegir S->[] si es pot derivar de forma indirecta
        self.ajustar_inicial_epsilon()
        print("Produccions epsilon eliminades i ajustades.")
        print(self.grammar)

        #B. Eliminar unitàries
        self.eliminar_unitaries()
        print("Produccions unitàries eliminades.")
        print(self.grammar)

        #C.Convertir terminals
        self.convertir_mixtes()
        print("Produccions de terminals convertides.")
        print(self.grammar)

        #D. Trencar regles llargues
        self.trencar_regles_no_bi()
        print("Regles llargues trencades.")
        print(self.grammar)

        return self.grammar #retornar gram en CNF (no format apte per CKY, cal transformació)
                            #Transformació en A_programa_principal.py
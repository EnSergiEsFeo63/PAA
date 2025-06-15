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
        for lhs, rhss in self.original.items():
            for rhs in rhss:
                if len(rhs) == 1:
                    if rhs[0].isupper():
                        return False  # A → B no CNF (B és no-terminal)
                elif len(rhs) == 2:
                    if not all(sym.isupper() for sym in rhs):
                        return False  # A → BC (ha de ser amb no-terminals)
                else:
                    return False
        return True


    def eliminar_epsiolon(self):
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



    

    def remove_units(self):
        unit_p=set()
        # Trobar les produccions unitàries
        for lhs, rhss in self.grammar.items():
            for rhs in rhss:
                if len(rhs) == 1 and rhs[0] in self.grammar:
                    unit_p.add((lhs, rhs[0]))

        changed = True
        while changed:
            changed = False
            for A,B in list(unit_p):
                for C, rhss in self.grammar.items():
                    if B == C:
                        for rhs in rhss:
                            if len(rhs) == 1 and rhs[0] in self.grammar:
                                if (A, rhs[0]) not in unit_p:
                                    unit_p.add((A, rhs[0]))
                                    changed = True

        new_grammar = {}
        for A,rhss in self.grammar.items():
            filt_rules= [] 
            for rhs in rhss:
                #long 1 i unic simbol no-terminal --> saltar
                if len(rhs) == 1 and rhs[0] in self.grammar:
                    continue 
                filt_rules.append(rhs)
            new_grammar[A] = filt_rules

        for A, B in unit_p:
            if A!=B:
                for rhs in self.grammar.get(B,[]):
                    if rhs not in new_grammar[A]:
                        new_grammar[A].append(rhs)
        self.grammar = new_grammar



    ######
    #PENDENT REVISAR
    ######
    def convert_terminals(self):
        terminal_map = {}
        new_rules = {}
        for lhs, rhss in self.grammar.items():
            new_rhss = []
            for rhs in rhss:
                if len(rhs) > 1:
                    new_rhs = []
                    for sym in rhs:
                        if sym not in self.grammar and not sym.isupper():
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
        self.grammar.update(new_rules)


    def break_long_rules(self):
        new_rules = {}
        for lhs, rhss in self.grammar.items():
            new_rhss = []
            for rhs in rhss:
                while len(rhs) > 2:
                    new_var = self._nova_var()
                    new_rules[new_var] = [[rhs[1], rhs[2]]]
                    rhs = [rhs[0], new_var] + rhs[3:]
                new_rhss.append(rhs)
            self.grammar[lhs] = new_rhss
        self.grammar.update(new_rules)


#REVISAT
    def to_cnf(self):
        if self.es_cnf():
            print("La gramàtica ja està en CNF.")
            return self.grammar
        print("Transformant la gramàtica a CNF...")

        #0. convertir cada producció de string a LLISTA de símbols
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
        #Aplicar les transformacions necessàries
        self.eliminar_epsiolon()
        print("Produccions epsilon eliminades.")

       
        print(self.grammar)
        self.remove_units()
        print("Produccions epsilon i unitàries eliminades.")
        print(self.grammar)
        self.convert_terminals()
        print("Produccions de terminals convertides.")
        print(self.grammar)
        self.break_long_rules()

        #convertir format apte per CKY
        final_grammar={}
        for lhs, rhss in self.grammar.items():
            final_grammar[lhs] = [''.join(rhs) for rhs in rhss]

        return final_grammar
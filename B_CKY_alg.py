import os

"""
Tot el programa serà bàsicament tota una classe ( per ara, si no va be doncs potser caldràn funcions fora de la classe, ns), 
ja veurem com farem la lectura de dades, pero per ara hem de programar l'algoritme en sí
"""
class CKY:
    def __init__(self,dades,nom_type):
        self.gramatica = dades #dades en format dict [aplicar func llegir dades]
        #print(self.gramatica)
        # Guardem si és determinista o probabilístic, ja que la extensió probabilística utilitza uns altres mètodes
        self.metode = 'det'
        if 'prob' in nom_type:
            self.metode = 'prob'

    
    def crear_taula(self,n):
        #La diferència entre aquestes dues taules és que la versió probabilística té dues llistes per cel·la: 
        # una per les paraules, i l'altra pels valors de probabilitat. 
        if self.metode == 'prob':
            taula = [[[[],[]] for i in range(n-j)]for j in range(n)]
        else:
            taula = [[[] for i in range(n-j)]for j in range(n)]
        
        return(taula)
    
    def resol(self, paraula):
        n = len(paraula)
        taula = self.crear_taula(n)
        #print(taula)
        taula = self.nivell1(taula,paraula)
        #print(taula)
        if self.metode == 'prob':
            return self.resol_prob(n,taula)
        else:
            return self.resol_det(n,taula)
        
    def combinacions(self, arg1, arg2):
        #Fem les combinacions de tots els valors de les dues cel·les
        #L'algoritme probabilistic necessita ademès que es fagin el producte de la probabilitat dels dos valors
        resultat = []
        if self.metode == 'prob':
            for idx1, nt1 in enumerate(arg1[0]):
                for idx2, nt2 in enumerate(arg2[0]):
                    element = nt1 + nt2
                    prob1 = arg1[1][idx1]
                    prob2 = arg2[1][idx2]
                    prob = prob1 * prob2
                    resultat.append((element, prob))
        else:
            if len(arg1) !=0 and len(arg2) != 0:
                for el1 in arg1:    
                    for el2 in arg2:
                        element = el1 + el2
                        resultat.append(element)
        return resultat
    
    def nivell1(self,taula,paraula):
        if self.metode == 'prob':
            for i in range(0,len(paraula)):
                for norma in self.gramatica:
                    for j, mot in enumerate(self.gramatica[norma][0]):
                        #print(paraula[i],mot)
                        if paraula[i] == mot:
                            taula[0][i][0].append(norma) #La primera llista de la cel·la és per el valor
                            taula[0][i][1].append(float(self.gramatica[norma][1][j])) # La segona és per la probabilitat
        else:
            for i in range(0,len(paraula)):
                for norma in self.gramatica:
                    if paraula[i] in self.gramatica[norma]:
                        taula[0][i].append(norma) #Per determinista només cal passar el valor i res més
        #print(taula)
        return taula

    def resol_det(self,n,taula):
        for i in range(0,n):
            for j in range(0,n-i):
                for k in range(0,i):
                    #print(taula[k][j])
                    #print(taula[i-k-1][j+k+1])
                    elements = self.combinacions(taula[k][j], taula[i-k-1][j+k+1])
                    #print(elements)
                    for valor in self.gramatica:
                        for element in elements:
                            if element in self.gramatica[valor]:
                                taula[i][j].append(valor)
        if 'S' in taula[n-1][0]:
            return True
        #print(taula)
        return False
    def resol_prob(self,n,taula):
        #print(self.gramatica)
        #print(taula)
        for i in range(0,n):
            for j in range(0,n-i):
                # Ensure the structure is properly initialized
                if not isinstance(taula[i][j], list) or len(taula[i][j]) < 2:
                    taula[i][j] = [[], []]
                
                for k in range(0,i):
                    # Skip if either table cell doesn't have the proper structure
                    if k >= len(taula) or j >= len(taula[k]) or not isinstance(taula[k][j], list) or len(taula[k][j]) < 2:
                        continue
                    if i-k-1 >= len(taula) or j+k+1 >= len(taula[i-k-1]) or not isinstance(taula[i-k-1][j+k+1], list) or len(taula[i-k-1][j+k+1]) < 2:
                        continue
                        
                    elements = self.combinacions(taula[k][j], taula[i-k-1][j+k+1])
                    for valor in self.gramatica:
                        for element, prob in elements:
                            for idx, mot in enumerate(self.gramatica[valor][0]):  # Changed j to idx to avoid shadowing
                                if element == mot:
                                    prob = prob * self.gramatica[valor][1][idx]
                                    if valor in taula[i][j][0]: 
                                        # Si el valor ja està en la taula, doncs agefem el valor el qual té la probabilitat més alta
                                        idx = taula[i][j][0].index(valor)
                                        if prob > taula[i][j][1][idx]:
                                            taula[i][j][1][idx] = prob
                                    else:
                                        taula[i][j][0] += [valor]
                                        taula[i][j][1] += [prob]
        #print(self.gramatica)
        #print(taula)   
        index = taula[n-1][0]                        
        if 'S' in index[0]:
            for count, lletra in enumerate(index[0]):
                if lletra == 'S':
                    probabilitat = index[1][count]
            #print(f"Probabilitat: {probabilitat}")
            return True,probabilitat
        return False,None
    

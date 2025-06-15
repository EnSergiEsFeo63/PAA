import os

"""
Tot el programa serà bàsicament tota una classe ( per ara, si no va be doncs potser caldràn funcions fora de la classe, ns), 
ja veurem com farem la lectura de dades, pero per ara hem de programar l'algoritme en sí
"""
class CKY:
    def __init__(self,nom):
        self.gramatica = self.llegir_dades(nom)
        self.metode = 'det'
        if 'prob' in nom:
            self.metode = 'prob'

        ### AQUI NO TENDRIA QUE RECIBIR TAMBIEN LA PALABRA?
        # Nah, rebrà la paraula amb resol, així pot resoldre més d'una paraula amb la mateixa gramàtica
        pass
    
    def crear_taula(self,n):
        if self.metode == 'det':
            taula = [[[] for i in range(n-j)]for j in range(n)]
        else:
            taula = [[[[],[]] for i in range(n-j)]for j in range(n)]
        return(taula)
    
    def resol(self, paraula):
        n = len(paraula)
        taula = self.crear_taula(n)
        #print(taula)
        taula = self.nivell1(taula,paraula)
        #print(taula)
        if self.metode == 'prob':
            return self.resol_prob(n,taula)
        return self.resol_det(n,taula)
        
    def combinacions(self, arg1, arg2):
        resultat = []
        if len(arg1) !=0 and len(arg2) != 0:
            for el1 in arg1:    
                for el2 in arg2:
                    element = el1 + el2
                    resultat.append(element)
        return resultat
    
    def nivell1(self,taula,paraula):
        for i in range(0,len(paraula)):
            for norma in self.gramatica:
                if paraula[i] in self.gramatica[norma]:
                    if self.metode == 'prob':
                        taula[0][i][0].append(norma)
                        taula[0][i][1].append(float(self.gramatica[norma][-1]))
                    else:
                        taula[0][i].append(norma)
        #print(taula)
        return taula
    def llegir_dades(self, nom):
        gramatica = {}
        nom += '.txt'
        directori = os.path.dirname(os.path.abspath(__file__))
        loc = os.path.join(directori,'fitxers')
        fitxer = os.path.join(loc, nom)
        with open(fitxer, 'r') as file:
            linees = file.readlines()
            #print(linees)
            #print(len(linees))
            for i in range(0,len(linees)):
                norma = linees[i][0]
                if norma not in gramatica:
                    gramatica[norma] = []
                frase = linees[i]
                paraula = ''
                n = 0
                while frase[n] != '>':
                    n+=1
                for j in range(n+1,len(frase)):
                    lletra = frase[j]
                    if lletra == '|' or j == len(frase)-1:
                        if i == len(linees)-1 and j == len(frase)-1:
                            paraula += lletra
                        gramatica[norma].append(paraula)
                        paraula = ''
                    elif lletra != '':
                        paraula += lletra    
        print(gramatica)
        return gramatica
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
        return False
        
    def resol_prob(self,n,taula):
        for valor in self.gramatica:
            self.gramatica[valor][1] = float(self.gramatica[valor][-1])
        #print(self.gramatica)
        for i in range(0,n):
            for j in range(0,n-i):
                for k in range(0,i):
                                        
                    elements = []
                    for idx1, nt1 in enumerate(taula[k][j][0]):
                        for idx2, nt2 in enumerate(taula[i-k-1][j+k+1][0]):
                            element = nt1 + nt2
                            prob1 = taula[k][j][1][idx1]
                            prob2 = taula[i-k-1][j+k+1][1][idx2]
                            prob = prob1 * prob2
                            elements.append((element, prob))
                    for valor in self.gramatica:
                        for element, prob1 in elements:
                            if element in self.gramatica[valor]:
                                prob2 = self.gramatica[valor][-1]
                                prob = prob1 * prob2
                                
                                if i == n-1 and 'S' in taula[n-1][0]:
                                    if prob > taula[i][j][1]:
                                        taula[i][j][0] = [valor]
                                        taula[i][j][1] = [prob]
                                    else:
                                        pass
                                else:
                                    taula[i][j][0] += [valor]
                                    taula[i][j][1] += [prob]

                                    
        #print(self.gramatica)                           
        if 'S' in taula[n-1][0]:
            print(f"Probabilitat: {taula[n-1][0][1]}")
            return True
        return False

            



e = CKY('gram_prob')
#print(e.gramatica)
print(e.resol('aaa')) 
 

        


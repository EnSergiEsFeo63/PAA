import os

"""
Tot el programa serà bàsicament tota una classe ( per ara, si no va be doncs potser caldràn funcions fora de la classe, ns), 
ja veurem com farem la lectura de dades, pero per ara hem de programar l'algoritme en sí
"""
class CKY:
    def __init__(self,nom):
        self.gramatica = self.llegir_dades(nom)
        #self.n = len(paraula)
        pass
    
    def crear_taula(self,n):
        taula = [[[] for i in range(n-j)]for j in range(n)]
        return(taula)
    
    def resol(self, paraula):
        n = len(paraula)
        taula = self.crear_taula(n)
        #print(taula)
        taula = self.nivell1(taula,paraula)
        #print(taula)
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
        #print(taula)
        
        return taula
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
                    taula[0][i].append(norma)
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
                gramatica[norma] = []
                frase = linees[i]
                paraula = ''
                n = 0
                while frase[n] != '>':
                    n+=1
                for j in range(n+1,len(frase)):
                    lletra = frase[j]
                    if lletra == '|' or j == len(frase)-1:
                        gramatica[norma].append(paraula)
                        paraula = ''
                    elif lletra != '':
                        paraula += lletra 
        print(gramatica)
        return gramatica



e = CKY('gram1')
e.resol('aaa')  
 

        


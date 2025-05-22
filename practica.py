import numpy as np
"""
Tot el programa serà bàsicament tota una classe ( per ara, si no va be doncs potser caldràn funcions fora de la classe, ns), 
ja veurem com farem la lectura de dades, pero per ara hem de programar l'algoritme en sí
"""
class CKY:
    def __init__(self, paraula):
        self.normes = {}
        #self.n = len(paraula)
        pass
    
    def crear_taula(self,n):
        taula = [[[] for i in range(n-j)]for j in range(n)]
        return(taula)
    
    def afegir_norma(self,index,norma):
        self.normes[index] = norma
        pass
    
    def resol(self, paraula):
        n = len(paraula)
        taula = self.crear_taula(n)
       
        taula = self.nivell1(taula,paraula)
        for i in range(0,n):
            for j in range(n-i):
                for k in range(i):
                    element = taula[k][j] + taula[i-k-1][j+k+1]
                    for valor in self.normes:
                        if element in self.normes[valor]:
                            taula[i][j].append(element)
        return taula
                    
    
    def nivell1(self,taula,paraula):
        for i in range(0,len(paraula)):
            for norma in self.normes:
                if paraula[i] in self.normes[norma]:
                    taula[0][i].append(norma)
        return taula

        


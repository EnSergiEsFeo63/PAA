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
    def resol(self, paraula):
        taula = self.crear_taula(self.n)
        l = len(paraula)
        taula = self.nivell1(taula,paraula)
        for i in range(0,l):
            for j in range(0, l-i):
                taula[0][i] = []
            for valor in self.normes.keys():
                if paraula[i] in self.normes[valor]:
                    taula[0][i] += [valor]
    def nivell1(self,taula,paraula):
        for i in range(0,len(paraula)):
            for norma in self.normes:
                if paraula[i] in self.normes[norma]:
                    taula[0][i].append(norma)
        return taula

        pass


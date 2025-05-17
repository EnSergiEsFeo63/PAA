import numpy as np
class CKY:
    def __init__(self, paraula):
        self.normes = {}
        self.n = len(paraula)
        pass
    def crear_taula(self,n):
        self.taula = np.zeros((n,n))
        
        return(self.taula)
    def afegir_norma(self,index,norma):
        self.normes[index] = [norma]
    def resol(self, paraula):
        taula = self.crear_taula(self.n)
        for i in range(0,len(paraula)):
            taula[0][i] = []
            for valor in self.normes.keys():
                if self.normes[valor] == paraula[i]:
                    taula[0][i] += [valor]

        pass


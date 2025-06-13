import os
#Get-Content .\fitxers\joc_proves.txt | python lectura.py
from pytokr import pytokr
import json



def llegir_dades(nom_fitxer):

    #accedir fitxer amb la gramàtica    
    nom_fitxer += '.txt'
    directori = os.path.dirname(os.path.abspath(__file__))
    loc = os.path.join(directori,'fitxers')
    fitxer = os.path.join(loc, nom_fitxer)

    gramatica = {}

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
                    if i == len(linees)-1 and j == len(frase)-1:
                        paraula += lletra
                    gramatica[norma].append(paraula)
                    paraula = ''
                elif lletra != '':
                    paraula += lletra    
    #print(gramatica)
    return gramatica



##########################################################################
#LLEGUIR JOCS DE PROVES
##########################################################################

def llegir_joc_proves_json(json_path='fitxers/joc_proves.json'):
    item = pytokr()
    ordre = item()
    dic_joc_proves = {}

    while ordre != 'finalitzar':
        if ordre == 'new_gram':
            nom_fitxer = item()
            if nom_fitxer not in dic_joc_proves:
                dic_joc_proves[nom_fitxer] = {}
            next = item()
            while next != 'end':
                paraula = next
                bool_p = item()
                bool_p= True if bool_p == 'T' else False  # Convertir a booleà
                if paraula not in dic_joc_proves[nom_fitxer]:
                    dic_joc_proves[nom_fitxer][paraula] = bool_p
                else:
                    print(f'La paraula "{paraula}" ja existeix a la gramàtica "{nom_fitxer}".')
                next = item()
        ordre = item()

    #guardar en JSON    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(dic_joc_proves, f, ensure_ascii=False, indent=2)
    print(f'Joc de proves guardat a {json_path}')


#convertir en JSON --> per poder interecturar input-ouput amb el programa principal

def carregar_joc_proves_json(json_path='fitxers/joc_proves.json'):
    with open(json_path, 'r', encoding='utf-8') as f:
        dic_joc_proves = json.load(f)
    return dic_joc_proves




if __name__ == "__main__":
    print("Llegint dades de joc de proves...")
    llegir_joc_proves_json()  





"""
from pytokr import pytokr
#em dona provlemes la merda de pytokr..... si executo amb python3 tot bé ;)
item= pytokr()
ordre=item()

dic_joc_proves = {}

while ordre != 'finalitzar':
    if ordre== 'new_gram':
        nom_fitxer = item()  # Nom del fitxer de gramàtica
        if nom_fitxer not in dic_joc_proves:
                dic_joc_proves[nom_fitxer] = {}
        next = item()
        while next != 'end':
            paraula= next
            bool_p= item()  # True o False
            if paraula not in dic_joc_proves[nom_fitxer]:
                dic_joc_proves[nom_fitxer][paraula] = bool_p
                #print (dic_joc_proves[nom_fitxer])
            else:
                print(f'La paraula "{paraula}" ja existeix a la gramàtica "{nom_fitxer}".')
        
            next = item()  # Llegir la següent ordre

    ordre = item()  # Llegir la següent ordre
        
print(dic_joc_proves)







#provar
q=llegir_dades('gram_2')
print(q)
"""



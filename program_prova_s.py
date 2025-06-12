################################################
#PROGRAMA PER LLEGUIR I EXECUTAR LLOCS DE PROVES
################################################
import os
from copy_prac_det_bona import CKY
from lectura import llegir_dades	
from trans_gram import GramTrans_CFGtoCNF

def main():
       
    print('Algorithm CKY - Prova de gramàtiques')

    #Nom fitxer de gramàtica
    print('Introdueix el nom de la gramàtica a provar:')
    print('Opcions:')
    for nom in os.listdir('fitxers'):
        if nom.endswith('.txt'):
            print(f'  {nom[:-4]}')
    nom_fitxer = input('Nom: ')

        
    #Llegir gramàtica
    gramatica = llegir_dades(nom_fitxer)

    #Transformar gramàtica a CNF
    print('Vols transformar la gramàtica a CNF? (S/N)')
    resposta = input('Resposta: ').strip().upper()
    if resposta == 'S':
        gramatica = GramTrans_CFGtoCNF(gramatica).to_cnf()
        print(gramatica)
    else:
        print('No s\'ha transformat la gramàtica a CNF.')

    print()
    #Crear objecte CKY
    cky = CKY(gramatica, nom_type='det')
    #print('Gramatica carregada correctament.')

    print('Introdueix la paraula a analitzar')
    paraula = input('Paraula: ')

    #Resoldre la paraula
    resultat = cky.resol(paraula)
    if resultat:
        print(f'La paraula "{paraula}" és vàlida segons la gramàtica.')
        
    else:
        print(f'La paraula "{paraula}" no és vàlida segons la gramàtica.')



###################
#FEINA PENDENT:
# - comprovar funcionament transformació a CNF de gram PROB
# - crear jocs de proves complets (amb paraules i gramàtiques) --> comporta canvi en lectura dades
# - Modificar programa principal- podem fer de dues maneres: iteratiu (provar paraula propia) o provar jocs de proves
# - Metode/ funcio per saber si gramtica en PROB o DET
###################






if __name__ == "__main__":
    main()
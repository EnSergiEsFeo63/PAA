################################################
#PROGRAMA PER LLEGUIR I EXECUTAR LLOCS DE PROVES
################################################
import os
from B_CKY_alg import CKY
from D_lectura import llegir_dades, carregar_joc_proves_json	
from C_Trans_gram import GramTrans_CFGtoCNF

def main():

    #Nom fitxer de gramàtica
    print('Introdueix el nom de la gramàtica a provar:')
    print('Opcions:')
    for nom in os.listdir('fitxers'):
        if nom.endswith('.txt'):
            print(f'  {nom[:-4]}')
    nom_fitxer = input('Nom: ')

        
    #Llegir gramàtica
    gramatica = llegir_dades(nom_fitxer)


    #TRANSDORMACIO OBLIGATORIIIIAAAAA
    #FER SERVIR METODE es_cnf per saber si la gramàtica és CNF
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

    print('-'*20)
    print('S\'han creat dues formes de prova:')
    print('1. Prova de paraules pròpies')
    print('2. Prova de jocs de proves')
    forma_prova = input('Tria una opció (1/2): ')
    print('-'*20)

    if forma_prova == '1':
        print ('1.PARAULES PROPIES')
        
        print('Introdueix la paraula a analitzar')
        paraula = input('Paraula: ')

        #Resoldre la paraula
        resultat = cky.resol(paraula)
        if resultat:
            print(f'La paraula "{paraula}" és vàlida segons la gramàtica.')
            
        else:
            print(f'La paraula "{paraula}" no és vàlida segons la gramàtica.')



    if forma_prova == '2':
        print ('2.JOCS DE PROVES')
        for p in dic_joc_proves[nom_fitxer]:
            print(f'Provant la paraula: {p}')
            resultat = cky.resol(p)
            if resultat:
                print(f'La paraula "{p}" és VÀLIDA segons la gramàtica.')
            else:
                print(f'La paraula "{p}" NO és vàlida segons la gramàtica.')

            #comprovar si la paraula és correcta segons el joc de proves
            
            print('Comprovació:', resultat == dic_joc_proves[nom_fitxer][p])
            






###################
#FEINA PENDENT:
# - comprovar funcionament transformació a CNF de gram PROB
# - crear jocs de proves complets (amb paraules i gramàtiques) --> comporta canvi en lectura dades
# - Modificar programa principal- podem fer de dues maneres: iteratiu (provar paraula propia) o provar jocs de proves
# - Metode/ funcio per saber si gramtica en PROB o DET
###################






if __name__ == "__main__":
    dic_joc_proves = carregar_joc_proves_json()  # Carregar jocs de proves
    #print(dic_joc_proves)
    main()
    
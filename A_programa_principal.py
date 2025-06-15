################################################
#PROGRAMA PER LLEGUIR I EXECUTAR LLOCS DE PROVES
################################################
import os
from B_CKY_alg import CKY
from D_lectura import llegir_dades, carregar_joc_proves_json, llegir_dades_prob	
from C_Trans_gram import GramTrans_CFGtoCNF

def main():

    #Nom fitxer de gramàtica
    prob = False
    print('Introdueix el nom de la gramàtica a provar:')
    print('Opcions:')
    for nom in os.listdir('fitxers'):
        if nom.endswith('.txt') and  not nom.startswith('joc_proves'):
            print(f'  {nom[:-4]}')
    nom_fitxer = input('Nom: ')

        
    #Llegir gramàtica
    if 'prob' in nom_fitxer:
        prob = True
        gramatica = llegir_dades_prob(nom_fitxer)
    else:
        gramatica = llegir_dades(nom_fitxer)


    #TRANSDORMACIO OBLIGATORIIIIAAAAA
    #FER SERVIR METODE es_cnf per saber si la gramàtica és CNF
    #Transformar gramàtica a CNF
    print(gramatica)
    gram= GramTrans_CFGtoCNF(gramatica) #fer millor, però per ara així funciona
    if gram.es_cnf() or prob:
        print('original:', gramatica)
        print('La gramàtica ja està en CNF.')
    else:
        print('La gramàtica NO està en CNF.')
        print('gram:ORIGINAL', gramatica)
        gramatica = GramTrans_CFGtoCNF(gramatica).to_cnf()
        print(gramatica)

    print()
    #Crear objecte CKY
    if prob:
        cky = CKY(gramatica, nom_type='prob')
    else:
        cky = CKY(gramatica, nom_type='det')
    #print('Gramatica carregada correctament.')

    print('-'*20)
    print('S\'han creat dues formes de prova:')
    print('1. Prova de paraules pròpies')
    print('2. Prova de jocs de proves')
    forma_prova = input('Tria una opció (1/2): ')
    print('-'*20)

    #Pots o generar la teva pròpia paraula, o utilitzar els que oferim en els jocs de prova
    if forma_prova == '1':
        print ('1.PARAULES PROPIES')
        
        print('Introdueix la paraula a analitzar')
        paraula = input('Paraula: ')

        #Resoldre la paraula
        if prob:
            resultat,probabilitat = cky.resol(paraula)
        else:
            resultat = cky.resol(paraula)
        if resultat:
            if prob:
                print(f'La paraula "{paraula}" és vàlida segons la gramàtica. Probabilitat: {probabilitat}')
            else:
                print(f'La paraula "{paraula}" és vàlida segons la gramàtica.')
            
        else:
            print(f'La paraula "{paraula}" no és vàlida segons la gramàtica.')



    if forma_prova == '2':
        print ('2.JOCS DE PROVES')
        for p in dic_joc_proves[nom_fitxer]:
            print(f'Provant la paraula: {p}')
            if prob:
                resultat,probabilitat = cky.resol(p)
            else:
                resultat = cky.resol(p)
            if resultat:
                if prob:
                    print(f'La paraula "{p}" és vàlida segons la gramàtica. Probabilitat: {probabilitat}')
                else:
                    print(f'La paraula "{p}" és vàlida segons la gramàtica.')
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
    
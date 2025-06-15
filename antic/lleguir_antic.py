
def llegir_dades_OLD_VERSION(nom_fitxer):

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
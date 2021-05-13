import copy
from pytomato.conversion_af_gr import (
    search_initial,
    search_non_terminal,
    search_terminal    
)

#from conversion_af_gr import search_initial,search_non_terminal,search_terminal,create_grammar_with_dict
"""Conversão de Texto x Objeto
Recebe duas strings, Gramática e Nome, do usuário e as
converte em objeto e insere na estrutura de dicionário.
"""
def texto_para_obj(text, nome):
    text = text.replace(' ', '')
    linhas = text.split('\n')
    gramatica = {}
    for linha in linhas:
        if '->' in linha:
            nomeEstado, estado = linha.split('->')
            transicoes = estado.split('|')

            gramatica[nomeEstado] = transicoes
    
    return {
        'nome': nome,
        'gramatica': gramatica
    }
"""Conversão de Objeto x Texto
Recebe um objeto, Gramática, da estrutura dicionário e converte
para formato padrão e retorna essa string.
"""
def obj_para_texto(objeto):
    gramatica = objeto['gramatica']
    texto = ''
    for nomeEstado, estado in gramatica.items():
        texto += nomeEstado + ' -> '
        for idx, transicao in enumerate(estado):
            if (idx < len(estado)-1):
                texto += transicao + ' | '
            else:
                texto += transicao + '\n'
    
    return texto

"""Reconhecimento de Expressão

Recebe uma string e um dicionario, expressão e gramática,
do usuário e retorna se a expressão é válida ou não.
"S -> aS | aA \n A -> bA | b"
-> aab
"""
def isValidExpression(expression, grammar, previousCharacter = None):
    terminalSymbolsList = search_terminal(grammar)
    nonTerminalSymbolsList = search_non_terminal(grammar)
    initialSymbol = search_initial(grammar)
    
    if (len(expression) == 0 and '&' in grammar[initialSymbol]):
        return True
    elif (len(expression) == 0):
        return False

    character = expression[0]

    if (len(expression) == 1):
        possibleTerminalSymbolsList = [v for l in grammar.values() for v in l]
        for possibleTerminalSymbol in possibleTerminalSymbolsList:
            if ((not previousCharacter) and len(possibleTerminalSymbol) == 1):
                if (character != possibleTerminalSymbol):
                    continue

                return True

            #if (not previousCharacter):
            #    breakpoint()
            #    return False

            #if (possibleTerminalSymbol != previousCharacter):
            #continue

            targetCharacter = possibleTerminalSymbol[-1]
            
            if (targetCharacter in terminalSymbolsList):
                return character == targetCharacter

            terminalSymbols = [v[1] for v in grammar[targetCharacter] if len(v) == 2]
            for terminalSymbol in terminalSymbols:
                if (terminalSymbol == character):
                    return True

        return False

    for c in expression:
        if not isValidExpression(c, grammar, previousCharacter):
            return False
        previousCharacter = c
    return True

def getcommonstart(seq):
    if not seq:return ""
    seq.sort()
    s1, s2 = seq[0], seq[-1]
    l = min(len(s1), len(s2))
    if l == 0 :
        return ""
    for i in range(l):
        if s1[i] != s2[i] :
            return s1[0:i]
    return s1[0:l]

"""Checar fatoraçao

Checa se uma gramatica ja esta fatorada
"""
def eh_fatorada(objeto):
    gramatica = objeto['gramatica'].copy()
    direto = False
    naodeterminismodireto = {}
    naodeterminismoindireto = {}
    fatorada = {
        'nome': objeto['nome']+"_fatorada",
        'gramatica': objeto['gramatica'].copy()
    }
    
    #Para cada não terminal da gramatica, checa se ele possue produções que iniciem da mesma forma (nao determinismo direto)
    #E para cada tipo de inicio igual encontrado, salva em um dicionario de listas
    for naoterminal in gramatica.keys():
        naodeterminismodireto[naoterminal] = []        
        temp = []
        for i in range(len(gramatica[naoterminal])):
            if len(gramatica[naoterminal][i]) == 1:
                continue
            for j in range(i+1,len(gramatica[naoterminal])):
                if len(gramatica[naoterminal][j]) == 1:
                    continue
                if gramatica[naoterminal][j].startswith(gramatica[naoterminal][i][0]):
                    if gramatica[naoterminal][i] not in (item for sublist in naodeterminismodireto[naoterminal] for item in sublist):
                        if gramatica[naoterminal][i] not in temp and len(gramatica[naoterminal][i]) > 1:
                            temp.append(gramatica[naoterminal][i])
                    if gramatica[naoterminal][j] not in (item for sublist in naodeterminismodireto[naoterminal] for item in sublist):
                        if gramatica[naoterminal][j] not in temp and len(gramatica[naoterminal][j]) > 1:
                            temp.append(gramatica[naoterminal][j])
            if temp != []:
                naodeterminismodireto[naoterminal].append(temp.copy())
                temp = []       
    #Atraves de derivações sucessivas das produções do nao terminal inicial, checa se elas possuem nao determinismo indireto
    #E para cada tipo de inicio igual encontrado no nao determinismo indireto, salva em um dicionario de listas
    naoterminais = list(gramatica)
    inicial = naoterminais[0]
    #tenta 2 derivações sucessivas no maximo
    for i in range(2):
        gramatica_derivada = copy.deepcopy(gramatica)
        for producao in gramatica[inicial]:
            for simbolo in producao:
                if simbolo in naoterminais:
                    if producao in gramatica_derivada[inicial]:
                        gramatica_derivada[inicial].remove(producao)
                    for p in gramatica[simbolo]:
                        gramatica_derivada[inicial].append(producao.replace(simbolo, p, 1))
                    break        
        gramatica = copy.deepcopy(gramatica_derivada)
        naodeterminismoindireto[inicial] = []
        temp = []
        for i in range(len(gramatica[inicial])):
            if len(gramatica[inicial][i]) == 1:
                continue
            for j in range(i+1,len(gramatica[inicial])):
                naoterminal_index = -1
                for n in naoterminais:  
                    a = gramatica[inicial][i].find(n)
                    if a != -1 and a < naoterminal_index or naoterminal_index == -1:
                        naoterminal_index = a
                if naoterminal_index == -1:
                    naoterminal_index = 0
                if len(gramatica[inicial][j]) == 1:
                    continue                
                if gramatica[inicial][j].startswith(gramatica[inicial][i][:naoterminal_index+1]):
                    if gramatica[inicial][i] not in (item for sublist in naodeterminismoindireto[inicial] for item in sublist):
                        if gramatica[inicial][i] not in temp and len(gramatica[inicial][i]) > 1:
                            temp.append(gramatica[inicial][i])
                    if gramatica[inicial][j] not in (item for sublist in naodeterminismoindireto[inicial] for item in sublist):
                        if gramatica[inicial][j] not in temp and len(gramatica[inicial][j]) > 1:
                            temp.append(gramatica[inicial][j])
            if temp != []:
                naodeterminismoindireto[inicial].append(temp.copy())
                temp = []
        if naodeterminismoindireto[inicial] != []:
            #substitui a gramatica atual pela derivada e adiciona o nao determinismo indireto para ser fatorado como o direto
            fatorada['gramatica'] = copy.deepcopy(gramatica)
            naodeterminismodireto[inicial].extend(naodeterminismoindireto[inicial])
            break        
    
    #checa se a gramatica esta fatorada
    esta_fatorada = True
    for naoterminal in naodeterminismodireto.keys():
        for lista in naodeterminismodireto[naoterminal]:
            if lista != []:
                esta_fatorada = False
    return esta_fatorada

"""Fatorar Gramatica

Fatora uma gramática, eliminando o não determinismo
"""
def fatorar_gramatica(objeto, tentativa):
    if tentativa == 3:
        objeto['nome'] = objeto['nome'] + "_falhanafatoracao"
        return objeto
    gramatica = objeto['gramatica'].copy()
    direto = False
    naodeterminismodireto = {}
    naodeterminismoindireto = {}
    fatorada = {
        'nome': objeto['nome']+"_fatorada",
        'gramatica': objeto['gramatica'].copy()
    }
    
    #Para cada não terminal da gramatica, checa se ele possue produções que iniciem da mesma forma (nao determinismo direto)
    #E para cada tipo de inicio igual encontrado, salva em um dicionario de listas
    for naoterminal in gramatica.keys():
        naodeterminismodireto[naoterminal] = []        
        temp = []
        for i in range(len(gramatica[naoterminal])):
            if len(gramatica[naoterminal][i]) == 1:
                continue
            for j in range(i+1,len(gramatica[naoterminal])):
                if len(gramatica[naoterminal][j]) == 1:
                    continue
                if gramatica[naoterminal][j].startswith(gramatica[naoterminal][i][0]):
                    if gramatica[naoterminal][i] not in (item for sublist in naodeterminismodireto[naoterminal] for item in sublist):
                        if gramatica[naoterminal][i] not in temp and len(gramatica[naoterminal][i]) > 1:
                            temp.append(gramatica[naoterminal][i])
                    if gramatica[naoterminal][j] not in (item for sublist in naodeterminismodireto[naoterminal] for item in sublist):
                        if gramatica[naoterminal][j] not in temp and len(gramatica[naoterminal][j]) > 1:
                            temp.append(gramatica[naoterminal][j])
            if temp != []:
                naodeterminismodireto[naoterminal].append(temp.copy())
                temp = []       
    #Atraves de derivações sucessivas das produções do nao terminal inicial, checa se elas possuem nao determinismo indireto
    #E para cada tipo de inicio igual encontrado no nao determinismo indireto, salva em um dicionario de listas
    naoterminais = list(gramatica)
    inicial = naoterminais[0]
    #tenta 2 derivações sucessivas no maximo
    for i in range(2):
        gramatica_derivada = copy.deepcopy(gramatica)
        for producao in gramatica[inicial]:
            for simbolo in producao:
                if simbolo in naoterminais:
                    if producao in gramatica_derivada[inicial]:
                        gramatica_derivada[inicial].remove(producao)
                    for p in gramatica[simbolo]:
                        gramatica_derivada[inicial].append(producao.replace(simbolo, p, 1))
                    break        
        gramatica = copy.deepcopy(gramatica_derivada)
        naodeterminismoindireto[inicial] = []
        temp = []
        for i in range(len(gramatica[inicial])):
            if len(gramatica[inicial][i]) == 1:
                continue
            for j in range(i+1,len(gramatica[inicial])):
                naoterminal_index = -1
                for n in naoterminais:  
                    a = gramatica[inicial][i].find(n)
                    if a != -1 and a < naoterminal_index or naoterminal_index == -1:
                        naoterminal_index = a
                if naoterminal_index == -1:
                    naoterminal_index = 0
                if len(gramatica[inicial][j]) == 1:
                    continue                
                if gramatica[inicial][j].startswith(gramatica[inicial][i][:naoterminal_index+1]):
                    if gramatica[inicial][i] not in (item for sublist in naodeterminismoindireto[inicial] for item in sublist):
                        if gramatica[inicial][i] not in temp and len(gramatica[inicial][i]) > 1:
                            temp.append(gramatica[inicial][i])
                    if gramatica[inicial][j] not in (item for sublist in naodeterminismoindireto[inicial] for item in sublist):
                        if gramatica[inicial][j] not in temp and len(gramatica[inicial][j]) > 1:
                            temp.append(gramatica[inicial][j])
            if temp != []:
                naodeterminismoindireto[inicial].append(temp.copy())
                temp = []
        if naodeterminismoindireto[inicial] != []:
            #substitui a gramatica atual pela derivada e adiciona o nao determinismo indireto para ser fatorado como o direto
            fatorada['gramatica'] = copy.deepcopy(gramatica)
            naodeterminismodireto[inicial].extend(naodeterminismoindireto[inicial])
            break        
    
    #checa se a gramatica esta fatorada
    esta_fatorada = True
    for naoterminal in naodeterminismodireto.keys():
        for lista in naodeterminismodireto[naoterminal]:
            if lista != []:
                esta_fatorada = False
    if not esta_fatorada:
        pass
    else:
        objeto['nome'] = objeto['nome'] + "_jaestavafatorada"
        return objeto
                
    #Fatora o nao determinismo direto (e indireto se foi adicionado)
    for naoterminal in naodeterminismodireto.keys():
        if naodeterminismodireto[naoterminal] != []:
            for lista in naodeterminismodireto[naoterminal]:
                alfa = getcommonstart(lista)
                novonaoterminal = naoterminal + "\'"
                fatorada['gramatica'][naoterminal].insert(0,alfa+novonaoterminal)
                fatorada['gramatica'][novonaoterminal] = []
                for item in lista:
                    fatorada['gramatica'][naoterminal].remove(item)
                    fatorada['gramatica'][novonaoterminal].append(item[len(alfa):])
                     
    if eh_fatorada(fatorada):
        return fatorada
    else:
        fatorada['nome'] = objeto['nome']
        resultado = fatorar_gramatica(fatorada,tentativa+1)
        return resultado        
                    
                    
                    

            
    

"""Teste
Main criado para testar as funções.
"""
tes =  { "S": ["aA", "bB", "cS"], "A": ["aS", "bC", "b", "cA"], "B": ["aC", "a", "bS", "cB"], "C": ["aB", "bA", "cC", "c"] }
if __name__ == '__main__':
    fatorar= "S -> AC | BC\n\
              A -> aD | cC\n\
              B -> aB | dD\n\
              C -> eC | eA\n\
              D -> fD | CB"
    #fatorar= "S -> bA | dA | d\n\
    #          A -> aA | cA"
              
    print(fatorar_gramatica(texto_para_obj(fatorar, 'fatorar'),0))

    texto= "S -> aA | bB | cS\n\
            A -> aS | bC | b | cA\n\
            B -> aC | a | bS | cB\n\
            C -> aB | bA | cC | c"

    print(texto_para_obj(texto, 'nome'))

    print(isValidExpression("a",  { "S": ["aA", "bB", "cS"], "A": ["aS", "bC", "b", "cA"], "B": ["aC", "a", "bS", "cB"], "C": ["aB", "bA", "cC", "c"] }, "a"))

    texto2="S -> & | &D | D | aA\n\
A -> D | bA | a\n\
B -> b | D\n\
S' -> & | &D | D | aA"
    print(texto_para_obj(texto2, 'nome'))
    caso_1="S -> Aa | b \n\
A -> Ac | Sd | a"
    caso_2="S -> Aa | Sb \n\
A -> Sd | d"
    obj = texto_para_obj(caso_1,'teste_recursao')
    GLC = create_grammar_with_dict(obj)
    obj_2 = texto_para_obj(caso_2,'teste_recursao_2')
    GLC_2 = create_grammar_with_dict(obj_2)
    # resultado igual slide https://moodle.ufsc.br/pluginfile.php/3837961/mod_resource/content/3/10-GLC-Algoritmos.pdf
    print(GLC.remove_left_recursions().asdict())
    print(GLC_2.remove_left_recursions().asdict())
from pytomato.conversion_af_gr import (
    search_initial,
    search_non_terminal,
    search_terminal
)
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


"""Teste
Main criado para testar as funções.
"""
tes =  { "S": ["aA", "bB", "cS"], "A": ["aS", "bC", "b", "cA"], "B": ["aC", "a", "bS", "cB"], "C": ["aB", "bA", "cC", "c"] }
if __name__ == '__main__':
    texto= "S -> aA | bB | cS\n\
            A -> aS | bC | b | cA\n\
            B -> aC | a | bS | cB\n\
            C -> aB | bA | cC | c"

    print(texto_para_obj(texto, 'nome'))

    print(isValidExpression("a",  { "S": ["aA", "bB", "cS"], "A": ["aS", "bC", "b", "cA"], "B": ["aC", "a", "bS", "cB"], "C": ["aB", "bA", "cC", "c"] }, "a"))

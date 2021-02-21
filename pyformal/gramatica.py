def traduzir_gramatica(text, nome):
    text = text.replace(' ', '')
    linhas = text.split('\n')
    gramatica = {}
    for linha in linhas:
        nomeEstado, estado = linha.split('->')
        transicoes = estado.split('|')
        
        gramatica[nomeEstado] = transicoes
    
    return {
        'nome': nome,
        'gramatica': gramatica
    }

def retornar_gramatica(objeto):
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

texto= "S -> aA | bB | cS\n\
        A -> aS | bC | b | cA\n\
        B -> aC | a | bS | cB\n\
        C -> aB | bA | cC | c"

print(retornar_gramatica(traduzir_gramatica(texto, 'nome')))

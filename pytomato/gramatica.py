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

"""Teste

Main criado para testar as funções.
"""
if __name__ == '__main__':
    texto= "S -> aA | bB | cS\n\
            A -> aS | bC | b | cA\n\
            B -> aC | a | bS | cB\n\
            C -> aB | bA | cC | c"

    print(texto_para_obj(texto, 'nome'))

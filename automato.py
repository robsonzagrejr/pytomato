def para_estrutura_de_dados(texto):
    linhas = texto.split("\n")
    '''
    numero_de_estados = linhas[0]
    estado_inicial = linhas[1]
    estados_de_aceitacao = linhas[2].split(',')
    alfabeto = linhas[3].split(',')
    '''
    transicoes = {}
    for t in range(4, len(linhas)):
        transicao = linhas[t].split(',')
        estado = transicao[0]
        
        if (not (estado in transicoes)):
            transicoes[estado] = {}

        simbolo_do_alfabeto = transicao[1]

        if (not (simbolo_do_alfabeto in transicoes[estado]) ):
            transicoes[estado][simbolo_do_alfabeto] = []

        estados_alvo = transicao[2].split('-')
        for e in estados_alvo:
            transicoes[estado][simbolo_do_alfabeto].append(e)

    return transicoes

def para_texto(n_estados, inicial, aceitacao, alfabeto, transicoes):
    texto = ''
    texto += n_estados + '\n'
    texto += inicial + '\n'
    texto += ','.join(aceitacao) + '\n'
    texto += ','.join(alfabeto) + '\n'
    for estado in transicoes:
        for simbolo in transicoes[estado]:
            texto += estado + ',' + simbolo + ',' + '-'.join(transicoes[estado][simbolo]) + '\n'
    return texto

'''
afnd_file = open("modelos/AFD", "r")
texto = (afnd_file.read())
transicoes = para_estrutura_de_dados(texto)
print(transicoes)
'''
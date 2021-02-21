def texto_para_obj(texto):
    linhas = texto.split("\n")
    estrutura = {}
    estrutura['n_estados'] = linhas[0]
    estrutura['inicial'] = linhas[1]
    estrutura['aceitacao'] = linhas[2].split(',')
    estrutura['alfabeto'] = linhas[3].split(',')
    transicoes = {}
    for t in range(4, len(linhas)):
        if (linhas[t]):
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
    estrutura['transicoes'] = transicoes
    return estrutura


def obj_para_texto(estrutura):
    texto = ''
    texto += estrutura['n_estados'] + '\n'
    texto += estrutura['inicial'] + '\n'
    texto += ','.join(estrutura['aceitacao']) + '\n'
    texto += ','.join(estrutura['alfabeto']) + '\n'
    for estado in estrutura['transicoes']:
        for simbolo in estrutura['transicoes'][estado]:
            texto += estado + ',' + simbolo + ',' + '-'.join(estrutura['transicoes'][estado][simbolo]) + '\n'
    return texto[:-1]

if __name__ == '__main__':
    afnd_file = open("modelos/AFD_com_epslon", "r")
    texto = (afnd_file.read())
    estrutura_de_dados = texto_para_obj(texto)
    print(estrutura_de_dados)
    novo_texto = obj_para_texto(estrutura_de_dados)
    print(novo_texto)


"""Conversão de Texto x Objeto

Recebe uma string, Autômato, no padrão definido e 
separada as informações presentes na sting e as salva
em cada atributo da estrutura de dicionário.
"""
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

"""Conversão de Objeto x Texto

Recebe um objeto, Autômato, da estrutura dicionário e converte
para formato padrão e retorna essa string, retirando a última
quebra de linha.
"""
def obj_para_texto(estrutura):
    texto = ''
    texto += str(estrutura['n_estados']) + '\n'
    if isinstance(estrutura['inicial'], list):
        texto += ','.join(estrutura['inicial']) + '\n'
    else:
        texto += estrutura['inicial'] + '\n'
    texto += ','.join(estrutura['aceitacao']) + '\n'
    texto += ','.join(estrutura['alfabeto']) + '\n'
    for estado in estrutura['transicoes']:
        for simbolo in estrutura['transicoes'][estado]:
            texto += estado + ',' + simbolo + ',' + '-'.join(estrutura['transicoes'][estado][simbolo]) + '\n'
    return texto[:-1]


"""Conversão de Tabela -> Objeto

Recebe uma tabela separada em linhas e cabeçalho.
Cada linha contem um estado, que a identifica, e as transicoes que saem desse estado a partir de cada simbolo do alfabeto.
O cabeçalho contem os simbolos do alfabeto, alem de um elemento vazio (''), e possivelmente, por conveniencia o epsilon (&)
A partir desses dados, a funcao monta um objeto, estrutura (dicionario) que descreve um automato, e entao o retorna
"""
def table_to_automaton(linhas, cabecalho):
    # inicializando variaveis
    estrutura = {}
    estado_inicial = ''
    estados_de_aceitacao = []
    alfabeto = []
    transicoes = {}

    # resgatar o alfabeto
    for c in range(1,len(cabecalho)):
        alfabeto.append(cabecalho[c]['name'])

    # para cada linha da tabela
    for linha in linhas:
        estado_label = linha['']

        estado_sem_seta_e_asterisco = estado_label.replace('->','').replace('*','')

        # encontrar estado inicial
        if estado_label.find("->") >= 0:
            estado_inicial = estado_sem_seta_e_asterisco
        
        # encontrar estados de aceitacao
        if estado_label.find("*") >= 0:
            estados_de_aceitacao.append(estado_sem_seta_e_asterisco)

        # resgatar cada transicao referente ao 'estado_sem_seta_e_asterisco'
        transicoes[estado_sem_seta_e_asterisco] = {}
        # para cada simbolo do alfabeto
        for simbolo_do_alfabeto in linha.keys():
            if simbolo_do_alfabeto != '':
                # pegar os estados alvo da transicao, caso haja algum estado alvo
                estados_alvo = linha[simbolo_do_alfabeto]
                if not estados_alvo in ['','\n','\r',None] :
                    # e entao resgatar todas as transicoes pelo simbolo do alfabeto em questao
                    estados_alvo_sem_chave_e_virgula = estados_alvo.replace('{','').replace('}','').split(',')
                    transicoes[estado_sem_seta_e_asterisco][simbolo_do_alfabeto] = estados_alvo_sem_chave_e_virgula

    estrutura['n_estados'] = str(len(linhas))
    estrutura['inicial'] = estado_inicial
    estrutura['aceitacao'] = estados_de_aceitacao
    estrutura['alfabeto'] = alfabeto
    estrutura['transicoes'] = transicoes

    return estrutura


"""Reconhecimento de sentenças em AF (caracter a carecter)

Os parametros sao: uma palavra, um automato no formato de dicionario, e um estado atual.
Para utilizar o procedimento, recomenda-se passar o estado inicial no campo 'estado_atual'.
A partir disso, a funcao faz chamadas recursivas ate consumir toda a palavra e entao
verifica se o automato se encontra em um estado de aceitacao.
Basta que um ramo de computacao aceite a palavra para que a funcao retorne 'True'.
"""
def _automato_aceita_palavra(palavra, automato, estado_atual=None):
    if not estado_atual:
        estado_atual = automato['inicial']

    if (len(palavra) == 0):
        return '', automato, estado_atual in automato['aceitacao'], estado_atual
    else:
        transicoes = automato['transicoes']
        if estado_atual in transicoes:
            simbolo_do_alfabeto = palavra[0]
            if simbolo_do_alfabeto in transicoes[estado_atual]:
                for estado_alvo in transicoes[estado_atual][simbolo_do_alfabeto]:
                    p = palavra[1:]
                    if not p:
                        p = ''
                    return p, automato, None, estado_alvo
        return '', automato, False, None


def automato_aceita_palavra(palavra, automato, estado_atual=None):
    aceita = False
    if palavra is None:
        palavra = ''
    while True:
        palavra, automato, aceita, estado_atual = _automato_aceita_palavra(palavra, automato, estado_atual)
        if aceita is not None:
            break
    return aceita, estado_atual


def renomear_estado_inicial(automato, novo_estado='S'):
    breakpoint()
    velho_inicial = automato['inicial']
    automato['inicial'] = novo_estado
    transicoes = {}
    for estado, trans in automato['transicoes'].items():
        estado_trans = {}
        for simbolo, estados in trans.items():
            estado_trans[simbolo] = []
            for e in estados:
                if e == velho_inicial:
                    estado_trans[simbolo].append(novo_estado)
                else:
                    estado_trans[simbolo].append(e)
        if estado == velho_inicial:
            estado = novo_estado
        transicoes[estado] = estado_trans
    automato['transicoes'] = transicoes 
    return automato  

"""Teste

Main criado para testar as funções.
"""
if __name__ == '__main__':
    #Conversao
    afnd_file = open("../examples/AFD_com_epslon", "r")
    texto = (afnd_file.read())
    estrutura_de_dados = texto_para_obj(texto)
    print(estrutura_de_dados)    
    import conversions    
    gram = conversions.afd_para_gramatica(estrutura_de_dados)
    print("--- gramatica: ---\n",gram)
    aut = conversions.gramatica_para_afd(gram)
    print("--- automato ---\n",aut)
    novo_texto = obj_para_texto(estrutura_de_dados)    
    

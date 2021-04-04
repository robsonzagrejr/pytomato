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
    texto += estrutura['n_estados'] + '\n'
    texto += estrutura['inicial'] + '\n'
    texto += ','.join(estrutura['aceitacao']) + '\n'
    texto += ','.join(estrutura['alfabeto']) + '\n'
    for estado in estrutura['transicoes']:
        for simbolo in estrutura['transicoes'][estado]:
            texto += estado + ',' + simbolo + ',' + '-'.join(estrutura['transicoes'][estado][simbolo]) + '\n'
    return texto[:-1]


"""Adição de prefixo em estados

Recebe um prefixo o qual será adicionado a todos os estados do automato.
Resolve o problema de estados com mesmo nome em operações envolvendo dois
automatos.
Retorna o mesmo automato porem com os estados posusindo tal prefixo.
"""
def _add_prefixo_estado(prefixo, automato):
    automato_r = {} 
    automato_r['n_estados'] = automato['n_estados']
    automato_r['inicial'] = f"{prefixo}_{automato['inicial']}"
    automato_r['aceitacao'] = [f"{prefixo}_{e}" for e in automato['aceitacao']]
    automato_r['alfabeto'] = automato['alfabeto']
    transicoes = {}
    for estado, trans in automato['transicoes'].items():
        estado_trans = {}
        for simbolo, estados in trans.items():
            estado_trans[simbolo] = [f"{prefixo}_{e}" for e in estados]
        transicoes[f"{prefixo}_{estado}"] = estado_trans
    automato_r['transicoes'] = transicoes    
    return automato_r


"""União de automatos

Recebe dois automatos e faz a união dos mesmos construindo
um automato com um novo estado de aceitação e inicial, fazendo episolon
transições. Renomeia os estados dos automatos que recebeu para previnir
possíveis erros.
"""
def uniao(automato_1, automato_2):
    automato_1_r = _add_prefixo_estado('a1', automato_1)
    automato_2_r = _add_prefixo_estado('a2', automato_2)

    automato_u = {}
    automato_u['n_estados'] = int(automato_1_r['n_estados']) + int(automato_1_r['n_estados']) + 2
    automato_u['inicial'] = 'S'
    automato_u['aceitacao'] = ['A']
    automato_u['alfabeto'] = list(set(automato_1_r['alfabeto'] + automato_2_r['alfabeto']))

    transicoes = automato_1_r['transicoes'].copy()
    transicoes.update(automato_2_r['transicoes'])
    transicoes[automato_u['inicial']] = {
        '&': [automato_1_r['inicial'], automato_2_r['inicial']]
    }
    antigo_aceitacao = automato_1_r['aceitacao'] + automato_2_r['aceitacao']
    for antigo_a in antigo_aceitacao:
        trans_antigo_a = transicoes.get(antigo_a, {})
        trans_antigo_a['&'] = automato_u['aceitacao']
        transicoes[antigo_a] = trans_antigo_a
    automato_u['transicoes'] = transicoes

    return automato_u 


"""Intercessão de automatos

Recebe dois automatos e faz a intercessão dos mesmos construindo
um automato com o estado de aceitação do automato_2 e inicial do automato_1,
fazendo episolon transições entre o final do automato_1 e o inicio do
automato_2. Renomeia os estados dos automatos que recebeu para previnir
possíveis erros.
"""
def intersecao(automato_1, automato_2):
    automato_1_r = _add_prefixo_estado('a1', automato_1)
    automato_2_r = _add_prefixo_estado('a2', automato_2)

    automato_i = {}
    automato_i['n_estados'] = int(automato_1_r['n_estados']) + int(automato_1_r['n_estados'])
    automato_i['inicial'] = automato_1_r['inicial']
    automato_i['aceitacao'] = automato_2_r['aceitacao']
    automato_i['alfabeto'] = list(set(automato_1_r['alfabeto'] + automato_2_r['alfabeto']))

    transicoes = automato_1_r['transicoes'].copy()
    transicoes.update(automato_2_r['transicoes'])
    antigo_aceitacao_1 = automato_1_r['aceitacao']
    for antigo_a in antigo_aceitacao_1:
        trans_antigo_a = transicoes.get(antigo_a, {})
        trans_antigo_a['&'] = [automato_2_r['inicial']]
        transicoes[antigo_a] = trans_antigo_a

    automato_i['transicoes'] = transicoes

    return automato_i


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

"""Teste

Main criado para testar as funções.
"""
if __name__ == '__main__':
    #Conversao
    afnd_file = open("AFD_com_epslon", "r")
    texto = (afnd_file.read())
    estrutura_de_dados = texto_para_obj(texto)
    print(estrutura_de_dados)    
    import conversions    
    gram = conversions.afd_para_gramatica(estrutura_de_dados)
    print("--- gramatica: ---\n",gram)
    aut = conversions.gramatica_para_afd(gram)
    print("--- automato ---\n",aut)
    novo_texto = obj_para_texto(estrutura_de_dados)    
    
    #Uniao e Intercessao
    print("=============Uniao===========")
    afd_file = open("AFND_sem_epsilon", "r")
    automato_1 = texto_para_obj(afd_file.read())
    automato_2 = automato_1.copy()
    print(uniao(automato_1, automato_2))

    print("=============Intersecao===========")
    print(intersecao(automato_1, automato_2))


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
    automato_u['alfabeto'] = list(
        set(
            automato_1_r['alfabeto']
            + automato_2_r['alfabeto']
            + ['&']
        )
    )

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
    automato_i['alfabeto'] = list(
        set(
            automato_1_r['alfabeto']
            + automato_2_r['alfabeto']
            +['&']
        )
    )

    transicoes = automato_1_r['transicoes'].copy()
    transicoes.update(automato_2_r['transicoes'])
    antigo_aceitacao_1 = automato_1_r['aceitacao']
    for antigo_a in antigo_aceitacao_1:
        trans_antigo_a = transicoes.get(antigo_a, {})
        trans_antigo_a['&'] = [automato_2_r['inicial']]
        transicoes[antigo_a] = trans_antigo_a

    automato_i['transicoes'] = transicoes

    return automato_i


"""Teste

Main criado para testar as funções.
"""
if __name__ == '__main__':
    print("=============Uniao===========")
    afd_file = open("../examples/AFND_sem_epsilon", "r")
    automato_1 = texto_para_obj(afd_file.read())
    automato_2 = automato_1.copy()
    print(uniao(automato_1, automato_2))

    print("=============Intersecao===========")
    print(intersecao(automato_1, automato_2))


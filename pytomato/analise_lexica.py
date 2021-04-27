import io
from .conversion_af_er import er_to_afd
from .operacoes_automato import uniao, afnd_para_afd
from .automato import obj_para_texto, automato_aceita_palavra, reordernar_nomes
from .operacoes_automato import uniao, _add_prefixo_estado, afnd_para_afd
from .conversion_af_er import er_to_afd

"""Conversão de Texto x Objeto
Recebe duas strings, expressoes Regulares e Nome, do usuário e as
insere na estrutura de dicionário.
"""
def text_to_obj(text, name):
    text_lines = io.StringIO(text)

    tokens = {}
    priority = 0
    for line in text_lines:
        line = line.replace('\n', ''). replace('\r', '')
        token_name = line.split(':')[0]
        token_er = line.split(':')[1]
        token = {
            'er': token_er,
            'prioridade': priority
        }
        tokens[token_name] = token
        priority += 1

    # Trocando tokens por ERs nas outras definicoes
    for token, val in tokens.items():
        for token_2, val_2 in tokens.items():
            if token != token_2:
                if token in val_2['er']:
                    er = val_2['er'].replace(token, val['er'])
                    val_2['er'] = er
                    tokens[token_2] = val_2

    '''
    super_automato = None
    for token in tokens:
        if super_automato == None:
            super_automato = token['afd']
        else:
            super_automato = uniao(super_automato, token['afd'])
    
    det_super_automato = afnd_para_afd(super_automato)
    print (obj_para_texto(det_super_automato))
    '''

    return {
        'nome': name,
        'texto': text,
        'tokens': tokens
    }


def extract_token_from_text(tokens, text):
    # Transformar em automatos
    automatons = []
    for token, er in tokens.items():
        automatons.append((
            int(er['prioridade']),
            {
                'name': token,
                'automato': er_to_afd(er['er']),
                'priority': er['prioridade']
            }
        ))

    # Ordernar de acordo com prioridade invertida
    # Maior o numero, maior a prioridade
    automatons = sorted(automatons)
    token_priorits = [(int(er['prioridade']), k) for k, er in tokens.items()]
    token_priorits = sorted(token_priorits, reverse=True)
    # Unir os automatos
    automaton_union = _add_prefixo_estado(
        automatons[0][1]['name'].replace('<', '|').replace('>','|'),
        automatons[0][1]['automato'],
        automatons[0][1]['name']
    )
    for automaton in automatons[1:]:
        automaton_union = uniao(
            automaton_union,
            automaton[1]['automato'],
            prefix_a1='',
            prefix_a2=automaton[1]['name'].replace('<', '|').replace('>','|'),
            #prefix_a2=automaton[1]['name'],
            aceitacao_prefix_a2=automaton[1]['name'],
            inicial=f"_{automaton_union['inicial']}",
        )
    # Determinizar
    automaton = afnd_para_afd(automaton_union)
    automaton = reordernar_nomes(automaton, tokens)

    # Identificar os lexemas
    lexemas = {}
    # Primeiro um caracter reservado 'espaço'
    text = text.replace('\n', ' ').replace('\r', ' ')
    for lex in text.split(' '):
        acepted, state = automato_aceita_palavra(lex, automaton)
        if acepted:
            for t in token_priorits:
                if t[1] in state:
                    token = t[1]
                    break
            lexemas[lex]= token 

    return lexemas, automaton
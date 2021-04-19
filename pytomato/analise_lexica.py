import io
"""Conversão de Texto x Objeto
Recebe duas strings, expressoes Regulares e Nome, do usuário e as
insere na estrutura de dicionário.
"""
def text_to_obj(text, name):
    text_lines = io.StringIO(text)

    tokens = {}
    priority = 0
    for line in text_lines:
        line = line[:-1]
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

    return {
        'nome': name,
        'texto': text,
        'tokens': tokens
    }



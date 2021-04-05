"""Conversão de Texto x Objeto
Recebe duas strings, expressão Regular e Nome, do usuário e as
insere na estrutura de dicionário.
"""
def texto_para_obj(text, nome):
    expressao_regular = text.replace(' ', '')
    
    return {
        'nome': nome,
        'expressao_regular': expressao_regular
    }


"""Conversão de Objeto x Texto
Recebe um objeto, Expressão Regular, da estrutura dicionário e converte
para formato padrão e retorna essa string.
"""
def obj_para_texto(objeto):
    expressao_regular = objeto['expressao_regular']
    return expressao_regular


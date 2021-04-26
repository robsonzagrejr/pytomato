import dash
import dash_bootstrap_components as dbc
import base64

import pytomato.analise_lexica as tomato_la

def upload_lexical_an(file_name, file_content, lexical_an_options,
        lexical_an_data):
    lexical_an_id = file_name.replace(' ','_').lower()

    alert_text = f'Linguagem {lexical_an_id} adicionada com sucesso :D'
    alert_type = 'success'
    keys = [v['value'] for v in lexical_an_options]
    if lexical_an_id in keys:
        alert_text = f"Linguagem '{lexical_an_id}' já existe :X"
        alert_type = 'danger'
    else:
        decoded_content = base64.b64decode( file_content.split(',')[1] ).decode("utf-8")
        lexical_an_obj = tomato_la.text_to_obj(decoded_content, lexical_an_id)
        # breakpoint()
        lexical_an_data[lexical_an_id] = lexical_an_obj

    alert = dbc.Alert(alert_text, color=alert_type, duration=1000)
    return lexical_an_data, alert


def add_lexical_an(lexical_an_name, lexical_an_text, lexical_an_options,
        lexical_an_data):
    lexical_an_id = lexical_an_name.replace(' ','_').lower()

    alert_text = f'Linguagem {lexical_an_name} adicionada com sucesso :D'
    alert_type = 'success'
    keys = [v['value'] for v in lexical_an_options]
    if lexical_an_id in keys:
        alert_text = f"Linguagem '{lexical_an_name}' já existe :X"
        alert_type = 'danger'
    else:
        lexical_an_obj = tomato_la.text_to_obj(lexical_an_text, lexical_an_id)
        # breakpoint()
        lexical_an_data[lexical_an_id] = lexical_an_obj

    alert = dbc.Alert(alert_text, color=alert_type, duration=1000)
    return lexical_an_data, alert


def update_lexical_an(lexical_an_text, lexical_an_selected, lexical_an_data):
    lexical_an_obj = tomato_la.text_to_obj(lexical_an_text, lexical_an_selected)
    lexical_an_data[lexical_an_selected] = lexical_an_obj

    alert_text = f"Linguagem '{lexical_an_selected}' atualizada com sucesso :)"
    alert_type = "success" 
    alert = dbc.Alert(alert_text, color=alert_type, duration=1000)
    return lexical_an_data, alert 


def remove_lexical_an(lexical_an_selected, lexical_an_data):
    lexical_an_data.pop(lexical_an_selected, None)
    alert_text = f"Linguagem '{lexical_an_selected}' deletada com sucesso :)"
    alert_type = "success" 
    alert = dbc.Alert(alert_text, color=alert_type, duration=1000)
    return lexical_an_data, alert


def extract_token(lenguage, text_to_parse):
    name = lenguage['nome']
    tokens = lenguage['tokens']
    #1º para cada ER' em token, tem q criar um automato finito
    #2º Para todos os automatos, tem q uni-los (<id>{0,1})
    #3º Determinizar o automato gigantesco
    #4º Para cada caracter do text_to_parse, _automato_aceita_palavra
    words_token, automaton = tomato_la.extract_token_from_text(tokens, text_to_parse)

    data = []
    for lex, token in words_token:
        data.append({
            'lexema': lex,
            'token': token
        })
    return data, {'type': 'AF', 'name':f'la_{name}', 'data': automaton}
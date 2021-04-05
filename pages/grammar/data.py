import dash
import dash_bootstrap_components as dbc
import base64

import pytomato.gramatica as tomato_gram
import pytomato.conversion_af_gr as tomato_gr_conv

def upload_grammar(file_name, file_content, grammar_options, grammar_data):
    grammar_id = file_name.replace(' ','_').lower()

    alert_text = f'Gramática {grammar_id} adicionada com sucesso :D'
    alert_type = 'success'
    keys = [v['value'] for v in grammar_options]
    if grammar_id in keys:
        alert_text = f"Gramática '{grammar_id}' já existe :X"
        alert_type = 'danger'
    else:
        decoded_content = base64.b64decode( file_content.split(',')[1] ).decode("utf-8")
        grammar_obj = tomato_gram.texto_para_obj(decoded_content, grammar_id)
        grammar_data[grammar_id] = grammar_obj

    alert = dbc.Alert(alert_text, color=alert_type, duration=1000)
    return grammar_data, alert


def add_grammar(grammar_name, grammar_text, grammar_options, grammar_data):
    grammar_id = grammar_name.replace(' ','_').lower()

    alert_text = f'Gramática {grammar_name} adicionada com sucesso :D'
    alert_type = 'success'
    keys = [v['value'] for v in grammar_options]
    if grammar_id in keys:
        alert_text = f"Gramática '{grammar_name}' já existe :X"
        alert_type = 'danger'
    else:
        grammar_obj = tomato_gram.texto_para_obj(grammar_text, grammar_id)
        grammar_data[grammar_id] = grammar_obj

    alert = dbc.Alert(alert_text, color=alert_type, duration=1000)
    return grammar_data, alert


def update_grammar(grammar_text, grammar_selected, grammar_data):
    grammar_obj = tomato_gram.texto_para_obj(grammar_text, grammar_selected)
    grammar_data[grammar_selected] = grammar_obj

    alert_text = f"Gramática '{grammar_selected}' atualizada com sucesso :)"
    alert_type = "success" 
    alert = dbc.Alert(alert_text, color=alert_type, duration=1000)
    return grammar_data, alert 


def remove_grammar(grammar_selected, grammar_data):
    grammar_data.pop(grammar_selected, None)
    alert_text = f"Gramática '{grammar_selected}' deletada com sucesso :)"
    alert_type = "success" 
    alert = dbc.Alert(alert_text, color=alert_type, duration=1000)
    return grammar_data, alert


def convert_grammar_to_af(grammar_selected, grammar_data, automaton_data):
    grammar = grammar_data[grammar_selected]
    new_automaton = tomato_gr_conv.gramatica_para_afd(grammar)
    name = f"gr_{grammar_selected}"
    helper_data = {
        'type': 'AF',
        'name': name,
        'data': new_automaton
    }
    alert_type = 'success'
    alert_text = f"Automato '{name}' criado a partir da Gramática com sucesso ! :)"
    if name in automaton_data.keys():
        alert_type = 'warning'
        alert_text = f"Automato '{name}' atualizado com sucesso ! :)"

    alert = dbc.Alert(alert_text, color=alert_type, duration=1000)

    return helper_data, alert


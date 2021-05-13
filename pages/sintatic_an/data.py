import dash
import dash_bootstrap_components as dbc
import base64

import pytomato.gramatica_lc as tomato_gram_lc

def upload_sintatic_an(file_name, file_content, sintatic_an_options,
        sintatic_an_data):
    sintatic_an_id = file_name.replace(' ','_').lower()

    alert_text = f'Gramática {sintatic_an_id} adicionada com sucesso :D'
    alert_type = 'success'
    keys = [v['value'] for v in sintatic_an_options]
    if sintatic_an_id in keys:
        alert_text = f"Gramática '{sintatic_an_id}' já existe :X"
        alert_type = 'danger'
    else:
        decoded_content = base64.b64decode( file_content.split(',')[1] ).decode("utf-8")
        sintatic_an_obj = tomato_gram.texto_para_obj(decoded_content,
                sintatic_an_id)
        sintatic_an_data[sintatic_an_id] = sintatic_an_obj

    alert = dbc.Alert(alert_text, color=alert_type, duration=1000)
    return sintatic_an_data, alert


def add_sintatic_an(sintatic_an_name, sintatic_an_text, sintatic_an_options,
        sintatic_an_data):
    sintatic_an_id = sintatic_an_name.replace(' ','_').lower()

    alert_text = f'Gramática {sintatic_an_name} adicionada com sucesso :D'
    alert_type = 'success'
    keys = [v['value'] for v in sintatic_an_options]
    if sintatic_an_id in keys:
        alert_text = f"Gramática '{sintatic_an_name}' já existe :X"
        alert_type = 'danger'
    else:
        sintatic_an_obj = tomato_gram.texto_para_obj(sintatic_an_text,
                sintatic_an_id)
        sintatic_an_data[sintatic_an_id] = sintatic_an_obj

    alert = dbc.Alert(alert_text, color=alert_type, duration=1000)
    return sintatic_an_data, alert


def update_sintatic_an(sintatic_an_text, sintatic_an_selected, sintatic_an_data):
    sintatic_an_obj = tomato_gram.texto_para_obj(sintatic_an_text, sintatic_an_selected)
    sintatic_an_data[sintatic_an_selected] = sintatic_an_obj

    alert_text = f"Gramática '{sintatic_an_selected}' atualizada com sucesso :)"
    alert_type = "success" 
    alert = dbc.Alert(alert_text, color=alert_type, duration=1000)
    return sintatic_an_data, alert 


def remove_sintatic_an(sintatic_an_selected, sintatic_an_data):
    sintatic_an_data.pop(sintatic_an_selected, None)
    alert_text = f"Gramática '{sintatic_an_selected}' deletada com sucesso :)"
    alert_type = "success" 
    alert = dbc.Alert(alert_text, color=alert_type, duration=1000)
    return sintatic_an_data, alert


def convert_sintatic_an_to_af(sintatic_an_selected, sintatic_an_data, automaton_data):
    sintatic_an = sintatic_an_data[sintatic_an_selected]
    new_automaton = tomato_gr_conv.gramatica_para_afd(sintatic_an)
    name = f"gr_{sintatic_an_selected}"
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


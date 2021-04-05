import dash
import dash_bootstrap_components as dbc
import base64

import pytomato.expressao_regular as tomato_er
import pytomato.conversion_af_er as tomato_er_conv

def upload_regular_exp(file_name, file_content, regular_exp_options,
        regular_exp_data):
    regular_exp_id = file_name.replace(' ','_').lower()

    alert_text = f'Expressão Regular {regular_exp_id} adicionada com sucesso :D'
    alert_type = 'success'
    keys = [v['value'] for v in regular_exp_options]
    if regular_exp_id in keys:
        alert_text = f"Expressão Regular'{regular_exp_id}' já existe :X"
        alert_type = 'danger'
    else:
        decoded_content = base64.b64decode( file_content.split(',')[1] ).decode("utf-8")
        regular_exp_obj = tomato_er.texto_para_obj(decoded_content, regular_exp_id)
        regular_exp_data[regular_exp_id] = regular_exp_obj

    alert = dbc.Alert(alert_text, color=alert_type, duration=1000)
    return regular_exp_data, alert


def add_regular_exp(regular_exp_name, regular_exp_text, regular_exp_options,
        regular_exp_data):
    regular_exp_id = regular_exp_name.replace(' ','_').lower()

    alert_text = f'Expressão Regular {regular_exp_name} adicionada com sucesso :D'
    alert_type = 'success'
    keys = [v['value'] for v in regular_exp_options]
    if regular_exp_id in keys:
        alert_text = f"Expressão Regular '{regular_exp_name}' já existe :X"
        alert_type = 'danger'
    else:
        regular_exp_obj = tomato_er.texto_para_obj(regular_exp_text, regular_exp_id)
        regular_exp_data[regular_exp_id] = regular_exp_obj

    alert = dbc.Alert(alert_text, color=alert_type, duration=1000)
    return regular_exp_data, alert


def update_regular_exp(regular_exp_text, regular_exp_selected, regular_exp_data):
    regular_exp_obj = tomato_er.texto_para_obj(regular_exp_text, regular_exp_selected)
    regular_exp_data[regular_exp_selected] = regular_exp_obj

    alert_text = f"Expressão Regular '{regular_exp_selected}' atualizada com sucesso :)"
    alert_type = "success" 
    alert = dbc.Alert(alert_text, color=alert_type, duration=1000)
    return regular_exp_data, alert 


def remove_regular_exp(regular_exp_selected, regular_exp_data):
    regular_exp_data.pop(regular_exp_selected, None)
    alert_text = f"Expressão Regular '{regular_exp_selected}' deletada com sucesso :)"
    alert_type = "success" 
    alert = dbc.Alert(alert_text, color=alert_type, duration=1000)
    return regular_exp_data, alert


def convert_regular_exp_to_af(regular_exp_selected, regular_exp_data):
    regular_exp_txt = regular_exp_data[regular_exp_selected]['expressao_regular']
    new_automaton= tomato_er_conv.er_to_afd(regular_exp_txt)
    name = f"er_{regular_exp_selected}"
    helper_data = {
        'type': 'AF',
        'name': name,
        'data': new_automaton
    }
    alert_type = 'success'
    alert_text = f"Automato '{name}' criado a partir da Expressão Regular com sucesso ! :)"
    if name in automaton_data.keys():
        alert_type = 'warning'
        alert_text = f"Automato '{name}' atualizado com sucesso ! :)"

    alert = dbc.Alert(alert_text, color=alert_type, duration=1000)

    return helper_data, alert

    return regular_exp_data, []



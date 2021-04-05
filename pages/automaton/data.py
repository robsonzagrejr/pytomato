import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

import base64
import pytomato.automato as tomato_auto

def upload_automaton(file_name, file_content, automaton_options, automaton_data):
        automaton_id = file_name.replace(' ','_').lower()

        alert_text = f'Automato {automaton_id} adicionada com sucesso :D'
        alert_type = 'success'
        keys = [v['value'] for v in automaton_options]
        if automaton_id in keys:
            alert_text = f"Automato '{automaton_id}' já existe :X"
            alert_type = 'danger'
        else:
            decoded_content = base64.b64decode( file_content.split(',')[1] ).decode("utf-8")
            automaton_obj = tomato_auto.texto_para_obj(decoded_content)
            automaton_data[automaton_id] = automaton_obj

        alert = dbc.Alert(alert_text, color=alert_type, duration=1000)
        return automaton_data, alert


def add_automaton(automaton_name, automaton_text, automaton_options, automaton_data):
    automaton_id = automaton_name.replace(' ','_').lower()

    alert_text = f'Automato {automaton_name} adicionado com sucesso :D'
    alert_type = 'success'
    keys = [v['value'] for v in automaton_options]
    if automaton_id in keys:
        alert_text = f"Automato '{automaton_name}' já existe :X"
        alert_type = 'danger'
    else:
        automaton_obj = tomato_auto.texto_para_obj(automaton_text)
        automaton_data[automaton_id] = automaton_obj

    alert = dbc.Alert(alert_text, color=alert_type, duration=1000)
    return automaton_data, alert


def update_automaton(automaton_text, automaton_selected, automaton_table_data,
        automaton_table_columns, automaton_data, triggered_id):
    
    automaton_obj = None
    if triggered_id == 'automaton-btn-update':
        automaton_obj = tomato_auto.texto_para_obj(automaton_text)
    else:
        automaton_obj = tomato_auto.table_to_automaton(automaton_table_data, automaton_table_columns)

    automaton_data[automaton_selected] = automaton_obj

    alert_text = f"Automato '{automaton_selected}' atualizado com sucesso :)"
    alert_type = "success" 
    alert = dbc.Alert(alert_text, color=alert_type, duration=1000)
    return automaton_data, alert 
        

def remove_automaton(automaton_selected, automaton_data):
    automaton_data.pop(automaton_selected, None)
    alert_text = f"Automato '{automaton_selected}' deletado com sucesso :)"
    alert_type = "success" 
    alert = dbc.Alert(alert_text, color=alert_type, duration=1000)
    return automaton_data, alert


def apply_operation_automaton(operation_type, operation_options, automaton_selected, automaton_second_selected, automaton_data):
    
    op_name = [v['label'] for v in operation_options if v['value'] == operation_type][0]
    alert_text = f"Operação {op_name} em automato '{automaton_selected}' efetuada com sucesso :)"
    alert_type = "success" 
    alert = dbc.Alert(alert_text, color=alert_type, duration=1000)
    
    return automaton_data, alert


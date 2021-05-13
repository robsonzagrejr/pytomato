import dash
import json
import dash_bootstrap_components as dbc
import dash_html_components as html
import base64

import pytomato.gramatica_lc as tomato_gram_lc

def upload_sintatic_an(file_name, file_content, sintatic_an_options,
        sintatic_an_data):
    sintatic_an_id = file_name.replace(' ','_').lower()

    alert_text = f'Gramática LC {sintatic_an_id} adicionada com sucesso :D'
    alert_type = 'success'
    keys = [v['value'] for v in sintatic_an_options]
    if sintatic_an_id in keys:
        alert_text = f"Gramática LC '{sintatic_an_id}' já existe :X"
        alert_type = 'danger'
    else:
        decoded_content = base64.b64decode( file_content.split(',')[1] ).decode("utf-8")
        sintatic_an_obj = tomato_gram_lc.text_to_obj(decoded_content, sintatic_an_id)
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
        alert_text = f"Gramática LC '{sintatic_an_name}' já existe :X"
        alert_type = 'danger'
    else:
        sintatic_an_obj = tomato_gram_lc.text_to_obj(sintatic_an_text, sintatic_an_id)
        sintatic_an_data[sintatic_an_id] = sintatic_an_obj

    alert = dbc.Alert(alert_text, color=alert_type, duration=1000)
    return sintatic_an_data, alert


def update_sintatic_an(sintatic_an_text, sintatic_an_selected, sintatic_an_data):
    sintatic_an_obj = tomato_gram_lc.text_to_obj(sintatic_an_text, sintatic_an_selected)
    sintatic_an_data[sintatic_an_selected] = sintatic_an_obj

    alert_text = f"Gramática LC '{sintatic_an_selected}' atualizada com sucesso :)"
    alert_type = "success" 
    alert = dbc.Alert(alert_text, color=alert_type, duration=1000)
    return sintatic_an_data, alert 


def remove_sintatic_an(sintatic_an_selected, sintatic_an_data):
    sintatic_an_data.pop(sintatic_an_selected, None)
    alert_text = f"Gramática LC '{sintatic_an_selected}' deletada com sucesso :)"
    alert_type = "success" 
    alert = dbc.Alert(alert_text, color=alert_type, duration=1000)
    return sintatic_an_data, alert


def print_items_table(sintatic_an_selected, sintatic_an_data):
    grammar = sintatic_an_data[sintatic_an_selected]
    complete_grammar = tomato_gram_lc.define_components(grammar)
    items = complete_grammar['itens']
    items_s = {key: {str(k): v for k, v in val.items()} for key, val in items.items()}
    columns = [{'name':'Estado', 'id':'state'}]
    data = []
    add_col_symbol = []
    for transition, action  in grammar['table']['table']['acao'].items():
        state, symbol = transition
        if symbol not in add_col_symbol:
            columns.append({'name': symbol, 'id':symbol})
            add_col_symbol.append(symbol)
        data.append((state,json.dumps({'state': state, symbol: action})))

    for transition, goto in grammar['table']['table']['goto'].items():
        state, symbol = transition
        if symbol not in add_col_symbol:
            columns.append({'name': symbol, 'id':symbol})
            add_col_symbol.append(symbol)
        data.append((state,json.dumps({'state': state, symbol: goto})))

    print(data)
    data_s = sorted(data)
    data_final = []
    state = data_s[0][0]
    aux = {}
    for d in data_s:
        if d[0] != state:
            data_final.append(aux)
            aux = {}
        state = d[0]
        aux.update(json.loads(d[1]))

    data_final.append(aux)

    return json.dumps(items_s, indent=4), columns, data_final

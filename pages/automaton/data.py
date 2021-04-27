import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

import base64
import pytomato.automato as tomato_auto
import pytomato.operacoes_automato as tomato_op_auto
import pytomato.conversion_af_gr as tomato_gr_conv
import pytomato.gramatica as tomato_gram

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
    if operation_type in ['union', 'intersection']:
        alert_text = f"Operação {op_name} entre '{automaton_selected}' e '{automaton_second_selected}' efetuada com sucesso :)"
        alert_type = "success" 
        if not automaton_second_selected: 
            alert_text = f"Operação {op_name} precisa ser entre dois automatos (- -)"
            alert_type = "danger" 
            alert = dbc.Alert(alert_text, color=alert_type, duration=1000)
            return automaton_data, alert

        if operation_type == 'union':
            automaton_1 = automaton_data[automaton_selected]
            automaton_2 = automaton_data[automaton_second_selected]
            automaton_u = tomato_op_auto.uniao(automaton_1, automaton_2)
            automaton_u_name = f"{automaton_selected}_u_{automaton_second_selected}"
            if automaton_u_name in automaton_data.keys():
                alert_text = f"Automato {automaton_u_name} atualizado com sucesso :)"
                alert_type = "warning" 

            automaton_data[automaton_u_name] = automaton_u

        elif operation_type == 'intersection':
            automaton_1 = automaton_data[automaton_selected]
            automaton_2 = automaton_data[automaton_second_selected]
            automaton_i = tomato_op_auto.intersecao(automaton_1, automaton_2)
            automaton_i_name = f"{automaton_selected}_i_{automaton_second_selected}"
            if automaton_i_name in automaton_data.keys():
                alert_text = f"Automato {automaton_i_name} atualizado com sucesso :)"
                alert_type = "warning" 

            automaton_data[automaton_i_name] = automaton_i


        alert = dbc.Alert(alert_text, color=alert_type, duration=1000)

    else:
        alert_text = f"Operação {op_name} em automato '{automaton_selected}' efetuada com sucesso :)"
        alert_type = "success" 
        if operation_type == 'minimization':
            automaton = automaton_data[automaton_selected]
            new_automaton = tomato_op_auto.minimiza_afd(automaton)
            new_automaton_name = f"min_{automaton_selected}"
            automaton_data[new_automaton_name] = new_automaton

        elif operation_type == 'determinization':
            automaton = automaton_data[automaton_selected]
            new_automaton = tomato_op_auto.afnd_para_afd(automaton)
            new_automaton_name = f"det_{automaton_selected}"
            automaton_data[new_automaton_name] = new_automaton


        alert = dbc.Alert(alert_text, color=alert_type, duration=1000)
    
    return automaton_data, alert


def convert_automaton_to_gr(automaton_selected, automaton_data, grammar_data):
    automaton = automaton_data[automaton_selected]
    name = f"af_{automaton_selected}"
    new_grammar = tomato_gr_conv.afd_para_gramatica(name, automaton)
    helper_data = {
        'type': 'GR',
        'name': name,
        'data': new_grammar
    }
    alert_type = 'success'
    alert_text = f"Gramática '{name}' criada a partir de Automato com sucesso ! :)"
    if name in automaton_data.keys():
        alert_type = 'warning'
        alert_text = f"Gramática '{name}' atualizada com sucesso ! :)"

    alert = dbc.Alert(alert_text, color=alert_type, duration=1000)

    return helper_data, alert

def check_word_in_automato(word, automaton_selected, automaton_data):
    if automaton_selected:
        automaton = automaton_data[automaton_selected]
        name = automaton_selected
        
        # commented out first attempt of implementation
        # grammar = tomato_gr_conv.afd_para_gramatica(name, automaton)['gramatica']
        # accept = tomato_gram.isValidExpression(word, grammar)
        
        # let's remove some undesirable characters
        if word:
            palavra = word.replace('\n','').replace('\r','')
        else:
            palavra = word
        
        accept, _ = tomato_auto.automato_aceita_palavra(word, automaton)
        alert_type = 'success'
        alert_text = f"Automato '{automaton_selected}' aceita palavra '{word}' ! :)"
        if not accept:
            alert_type = 'danger'
            alert_text = f"Automato '{automaton_selected}' não reconhece palavra '{word}' ! :X"
    else:
        alert_type = 'warning'
        alert_text = f"Selecione um Automato !!"

    alert = dbc.Alert(alert_text, color=alert_type, duration=2000)
    return alert

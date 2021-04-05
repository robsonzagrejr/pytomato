import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

import base64
import pytomato.automato as tomato_auto
import pytomato.operacoes_automato as tomato_op_auto

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
            print('APPLY Minimization') #FIXME

        elif operation_type == 'determinization':
            print('APPLY Determinization') #FIXME


        alert = dbc.Alert(alert_text, color=alert_type, duration=1000)
    
    return automaton_data, alert


def make_graph(automaton_selected, automaton_data):
    graph_js = """
    // create an array with nodes
    var nodes = new vis.DataSet([
      { id: 1, label: "Node 1" },
      { id: 2, label: "Node 2" },
      { id: 3, label: "Node 3" },
      { id: 4, label: "Node 4" },
      { id: 5, label: "Node 5" },
    ]);

    // create an array with edges
    var edges = new vis.DataSet([
      { from: 1, to: 3 },
      { from: 1, to: 2 },
      { from: 2, to: 4 },
      { from: 2, to: 5 },
      { from: 3, to: 3 },
    ]);

    // create a network
    var container = document.getElementById("mynetwork");
    var data = {
      nodes: nodes,
      edges: edges,
    };
    var options = {};
    var network = new vis.Network(container, data, options);

    """

    graph_js= 'alert("KAKAK");'

    return graph_js

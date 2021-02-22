import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import base64

import pytomato.automato as tomato_auto

def register_callbacks(app):
    @app.callback(
        [
            Output('automaton-download','download'),
            Output('automaton-download', 'href'),
        ],
        [
            Input('automaton-dropdown', 'value'),
            Input('store-automaton', 'data')
        ],
    )
    def automaton_download(automaton_selected, automaton_data):
        if automaton_selected and automaton_selected in automaton_data.keys():
            data = tomato_auto.obj_para_texto(automaton_data[automaton_selected])
            data = data.replace('\n', "%0D%0A");
            data = f"data:text/plain;UTF-8,{data}"
            return f"{automaton_selected}", data
        return '', ''


    @app.callback(
        [
            Output('automaton-input', 'value'),
            Output('automaton-text-area', 'value'),
            Output('automaton-input', 'disabled'),
            Output('automaton-btn-add', 'style'),
            Output('automaton-btn-update', 'style')
        
        ],
        [
            Input('automaton-dropdown', 'value'),
            Input('automaton-dropdown', 'options'),
            Input('store-automaton', 'data')
        ]
    )
    def select_automaton(automaton_selected, automaton_options, automaton_data):
        if automaton_options:
            keys = [v['value'] for v in automaton_options]
            if automaton_selected in keys:
                automaton_text = tomato_auto.obj_para_texto(automaton_data[automaton_selected])
                return automaton_selected, automaton_text, True, {'display': 'none'}, {}
        return "", "", False, {}, {'display': 'none'}


    @app.callback(
        Output('automaton-dropdown', 'options'),
        [
            Input('store-automaton', 'data'),
        ],
    )
    def update_options(automaton_data):
        options = [{'label': k, 'value': k} for k in automaton_data.keys()]
        return options


    @app.callback(
        [
            Output('store-automaton', 'data'),
            Output('automaton-alert', 'children'),
        ],
        [
            Input('automaton-upload','contents'),
            Input('automaton-upload', 'filename'),
            Input('automaton-btn-add', 'n_clicks'),
            Input('automaton-btn-update', 'n_clicks'),
            Input('automaton-btn-rm', 'n_clicks'),
        ],
        [
            State('automaton-dropdown', 'value'),
            State('automaton-dropdown', 'options'),
            State('automaton-input', 'value'),
            State('automaton-text-area', 'value'),
            State('store-automaton', 'data')
        ]
    )
    def update_automaton_data(
            file_content,
            file_name,
            add_click,
            update_click,
            rm_click,
            automaton_selected,
            automaton_options,
            automaton_name,
            automaton_text,
            automaton_data
        ):
        ctx = dash.callback_context
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if triggered_id == 'automaton-upload' or triggered_id == 'automaton-filename':
            if file_name:
                automaton_id = file_name.replace(' ','_').lower()

                alert_text = f'Gramática {automaton_name} adicionada com sucesso :D'
                alert_type = 'success'
                keys = [v['value'] for v in automaton_options]
                if automaton_id in keys:
                    alert_text = f"Gramática '{automaton_name}' já existe :X"
                    alert_type = 'danger'
                else:
                    decoded_content = base64.b64decode( file_content.split(',')[1] ).decode("utf-8")
                    automaton_obj = tomato_auto.texto_para_obj(decoded_content)
                    automaton_data[automaton_id] = automaton_obj

                alert = dbc.Alert(alert_text, color=alert_type, duration=4000)
                return automaton_data, alert

        elif triggered_id == 'automaton-btn-add' and automaton_name:
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

            alert = dbc.Alert(alert_text, color=alert_type, duration=4000)
            return automaton_data, alert

        elif triggered_id == 'automaton-btn-update' and automaton_selected:
            automaton_obj = tomato_auto.texto_para_obj(automaton_text)
            automaton_data[automaton_selected] = automaton_obj

            alert_text = f"Automato '{automaton_selected}' atualizado com sucesso :)"
            alert_type = "success" 
            alert = dbc.Alert(alert_text, color=alert_type, duration=4000)
            return automaton_data, alert 

        elif triggered_id == 'automaton-btn-rm' and automaton_selected:
            automaton_data.pop(automaton_selected, None)
            alert_text = f"Automato '{automaton_selected}' deletado com sucesso :)"
            alert_type = "success" 
            alert = dbc.Alert(alert_text, color=alert_type, duration=4000)
            return automaton_data, alert

        return automaton_data, []


    @app.callback(
        [
            Output('automaton-table', 'data'),
            Output('automaton-table', 'columns'),
        ],
        [
            Input('automaton-dropdown', 'value'),
            Input('store-automaton', 'data'),
        ],
    )
    def update_automaton_table(automaton_selected, automaton_data):
        if automaton_selected in automaton_data.keys():
            automaton = automaton_data[automaton_selected]
            columns = [
                {
                    'name': l,
                    'id':l,
                    #'editable': True
                }
                for l in [''] + automaton['alfabeto']
            ]
            data = []
            for estado, trans in automaton['transicoes'].items():
                row = {} 
                estado_label = estado
                if estado == automaton['inicial']:
                    estado_label = '->' + estado_label
                if estado in automaton['aceitacao']:
                    estado_label = '*' + estado_label

                row[''] = estado_label
                for letra, estado_alvo in trans.items():
                    alvo = "{"+','.join(estado_alvo)+"}"
                    row[letra] = alvo
                data.append(row)
            return data, columns
        return [], []

import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import base64

import pytomato.expressao_regular as tomato_er
import pytomato.conversion_af_er as tomato_er_conv

"""Funções de Callback

Funções que definem as triggers e execução de cada callback.
"""
def register_callbacks(app):
    @app.callback(
        [
            Output('regular-exp-download','download'),
            Output('regular-exp-download', 'href'),
        ],
        [
            Input('regular-exp-dropdown', 'value'),
            Input('store-regular-exp', 'data'),
        ],
    )
    def regular_exp_download(regular_exp_selected, regular_exp_data):
        """Callback Download Gramática

        Callback para chamada de download de gramáticas
        em arquivo de texto.
        """
     
        if regular_exp_selected and regular_exp_selected in regular_exp_data.keys():
            data = tomato_er.obj_para_texto(regular_exp_data[regular_exp_selected])
            data = data.replace('\n', "%0D%0A");
            data = f"data:text/plain;UTF-8,{data}"
            return f"{regular_exp_selected}", data
        return '', ''

    @app.callback(
        [
            Output('regular-exp-input', 'value'),
            Output('regular-exp-text-area', 'value'),
            Output('regular-exp-input', 'disabled'),
            Output('regular-exp-btn-add', 'style'),
            Output('regular-exp-btn-update', 'style')
        
        ],
        [
            Input('regular-exp-dropdown', 'value'),
            Input('regular-exp-dropdown', 'options'),
            Input('store-regular-exp', 'data')
        ]
    )
    def select_regular_exp(regular_exp_selected, regular_exp_options, regular_exp_data):
        """Callback Seleção Gramática

        Callback para gerenciar a seleção e display do
        dropdown das gramáticas.
        """
    
        if regular_exp_options:
            keys = [v['value'] for v in regular_exp_options]
            if regular_exp_selected in keys:
                regular_exp_text = tomato_er.obj_para_texto(regular_exp_data[regular_exp_selected])
                return regular_exp_selected, regular_exp_text, True, {'display': 'none'}, {}
        return "", "", False, {}, {'display': 'none'}


    @app.callback(
        Output('regular-exp-dropdown', 'options'),
        [
            Input('store-regular-exp', 'data'),
        ],
    )
    def update_options(regular_exp_data):
        options = [{'label': k, 'value': k} for k in regular_exp_data.keys()]
        return options


    @app.callback(
        [
            Output('store-regular-exp-helper', 'data'),
            Output('regular-exp-alert', 'children'),
        ],
        [
            Input('regular-exp-upload','contents'),
            Input('regular-exp-upload', 'filename'),
            Input('regular-exp-btn-add', 'n_clicks'),
            Input('regular-exp-btn-update', 'n_clicks'),
            Input('regular-exp-btn-rm', 'n_clicks'),
            Input('regular-exp-btn-convert-af', 'n_clicks'),
        ],
        [
            State('regular-exp-dropdown', 'value'),
            State('regular-exp-dropdown', 'options'),
            State('regular-exp-input', 'value'),
            State('regular-exp-text-area', 'value'),
            State('store-regular-exp', 'data'),
            State('store-automaton', 'data'),
        ]
    )
    def update_regular_exp_data(
            file_content,
            file_name,
            add_click,
            update_click,
            rm_click,
            er_convert_af_click,

            regular_exp_selected,
            regular_exp_options,
            regular_exp_name,
            regular_exp_text,
            regular_exp_data,
            automaton_data,
        ):
        """Callback Update Gramática

        Callback que gerencia criação, exclusão, upload, alteração
        de gramática.
        """
    
        ctx = dash.callback_context
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if triggered_id == 'regular-exp-upload' or triggered_id == 'regular-exp-filename':
            if file_name:
                regular_exp_id = file_name.replace(' ','_').lower()

                alert_text = f'Expressão Regular {regular_exp_name} adicionada com sucesso :D'
                alert_type = 'success'
                keys = [v['value'] for v in regular_exp_options]
                if regular_exp_id in keys:
                    alert_text = f"Expressão Regular'{regular_exp_name}' já existe :X"
                    alert_type = 'danger'
                else:
                    decoded_content = base64.b64decode( file_content.split(',')[1] ).decode("utf-8")
                    regular_exp_obj = tomato_er.texto_para_obj(decoded_content, regular_exp_id)
                    regular_exp_data[regular_exp_id] = regular_exp_obj

                alert = dbc.alert(alert_text, color=alert_type, duration=1000)
                return regular_exp_data, alert

        elif triggered_id == 'regular-exp-btn-add' and regular_exp_name:
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

        elif triggered_id == 'regular-exp-btn-update' and regular_exp_selected:
            regular_exp_obj = tomato_er.texto_para_obj(regular_exp_text, regular_exp_selected)
            regular_exp_data[regular_exp_selected] = regular_exp_obj

            alert_text = f"Expressão Regular '{regular_exp_selected}' atualizada com sucesso :)"
            alert_type = "success" 
            alert = dbc.Alert(alert_text, color=alert_type, duration=1000)
            return regular_exp_data, alert 

        elif triggered_id == 'regular-exp-btn-rm' and regular_exp_selected:
            regular_exp_data.pop(regular_exp_selected, None)
            alert_text = f"Expressão Regular '{regular_exp_selected}' deletada com sucesso :)"
            alert_type = "success" 
            alert = dbc.Alert(alert_text, color=alert_type, duration=1000)
            return regular_exp_data, alert

        elif (triggered_id == 'regular-exp-btn-convert-af' and
             regular_exp_selected and regular_exp_selected in regular_exp_data.keys()):

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


    #Conversoes
    @app.callback(
        Output('store-regular-exp', 'data'),
        [
            Input('store-regular-exp-helper', 'data'),
        ],
        [
            State('store-regular-exp', 'data')
        ]
    )
    def regular_exp_data(regular_exp_data_helper, regular_exp_data):
        """Callback Download Gramática

        """
        if 'type' not in regular_exp_data_helper.keys():
            return regular_exp_data_helper
     
        return regular_exp_data


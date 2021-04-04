import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import base64

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
    def grammar_download(grammar_selected, grammar_data):
        """Callback Download Gramática

        Callback para chamada de download de gramáticas
        em arquivo de texto.
        """
     
        if grammar_selected and grammar_selected in grammar_data.keys():
            #data = tomato_gram.obj_para_texto(grammar_data[grammar_selected])
            data = ''
            data = data.replace('\n', "%0D%0A");
            data = f"data:text/plain;UTF-8,{data}"
            return f"{grammar_selected}", data
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
    def select_grammar(grammar_selected, grammar_options, grammar_data):
        """Callback Seleção Gramática

        Callback para gerenciar a seleção e display do
        dropdown das gramáticas.
        """
    
        if grammar_options:
            keys = [v['value'] for v in grammar_options]
            if grammar_selected in keys:
                #grammar_text = tomato_gram.obj_para_texto(grammar_data[grammar_selected])
                grammar_text = ""
                return grammar_selected, grammar_text, True, {'display': 'none'}, {}
        return "", "", False, {}, {'display': 'none'}


    @app.callback(
        Output('regular-exp-dropdown', 'options'),
        [
            Input('store-regular-exp', 'data'),
        ],
    )
    def update_options(grammar_data):
        options = [{'label': k, 'value': k} for k in grammar_data.keys()]
        return options


    @app.callback(
        [
            Output('store-regular-exp', 'data'),
            Output('regular-exp-alert', 'children'),
        ],
        [
            Input('regular-exp-upload','contents'),
            Input('regular-exp-upload', 'filename'),
            Input('regular-exp-btn-add', 'n_clicks'),
            Input('regular-exp-btn-update', 'n_clicks'),
            Input('regular-exp-btn-rm', 'n_clicks'),
        ],
        [
            State('regular-exp-dropdown', 'value'),
            State('regular-exp-dropdown', 'options'),
            State('regular-exp-input', 'value'),
            State('regular-exp-text-area', 'value'),
            State('store-regular-exp', 'data')
        ]
    )
    def update_grammar_data(
            file_content,
            file_name,
            add_click,
            update_click,
            rm_click,
            grammar_selected,
            grammar_options,
            grammar_name,
            grammar_text,
            grammar_data
        ):
        """Callback Update Gramática

        Callback que gerencia criação, exclusão, upload, alteração
        de gramática.
        """
    
        ctx = dash.callback_context
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if triggered_id == 'regular-exp-upload' or triggered_id == 'regular-exp-filename':
            if file_name:
                grammar_id = file_name.replace(' ','_').lower()

                alert_text = f'Gramática {grammar_name} adicionada com sucesso :D'
                alert_type = 'success'
                keys = [v['value'] for v in grammar_options]
                if grammar_id in keys:
                    alert_text = f"Gramática '{grammar_name}' já existe :X"
                    alert_type = 'danger'
                else:
                    decoded_content = base64.b64decode( file_content.split(',')[1] ).decode("utf-8")
                    #grammargrammar_obj = tomato_gram.texto_para_obj(decoded_content, grammar_id)
                    grammar_obj = {}
                    grammar_data[grammar_id] = grammar_obj

                alert = dbc.Alert(alert_text, color=alert_type, duration=4000)
                return grammar_data, alert

        elif triggered_id == 'regular-exp-btn-add' and grammar_name:
            grammar_id = grammar_name.replace(' ','_').lower()

            alert_text = f'Gramática {grammar_name} adicionada com sucesso :D'
            alert_type = 'success'
            keys = [v['value'] for v in grammar_options]
            if grammar_id in keys:
                alert_text = f"Gramática '{grammar_name}' já existe :X"
                alert_type = 'danger'
            else:
                #grammar_obj = tomato_gram.texto_para_obj(grammar_text, grammar_id)
                grammar_obj = {}
                grammar_data[grammar_id] = grammar_obj

            alert = dbc.Alert(alert_text, color=alert_type, duration=4000)
            return grammar_data, alert

        elif triggered_id == 'regular-exp-btn-update' and grammar_selected:
            #grammar_obj = tomato_gram.texto_para_obj(grammar_text, grammar_selected)
            grammar_obj = {}
            grammar_data[grammar_selected] = grammar_obj

            alert_text = f"Gramática '{grammar_selected}' atualizada com sucesso :)"
            alert_type = "success" 
            alert = dbc.Alert(alert_text, color=alert_type, duration=4000)
            return grammar_data, alert 

        elif triggered_id == 'regular-exp-btn-rm' and grammar_selected:
            grammar_data.pop(grammar_selected, None)
            alert_text = f"Gramática '{grammar_selected}' deletada com sucesso :)"
            alert_type = "success" 
            alert = dbc.Alert(alert_text, color=alert_type, duration=4000)
            return grammar_data, alert

        return grammar_data, []


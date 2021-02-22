import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import base64

import pytomato.gramatica as tomato_gram

def register_callbacks(app):
    @app.callback(
        [
            Output('grammar-download','download'),
            Output('grammar-download', 'href'),
        ],
        [
            Input('grammar-dropdown', 'value'),
            Input('store-grammar', 'data'),
        ],
    )
    def grammar_download(grammar_selected, grammar_data):
        if grammar_selected and grammar_selected in grammar_data.keys():
            data = tomato_gram.obj_para_texto(grammar_data[grammar_selected])
            data = data.replace('\n', "%0D%0A");
            data = f"data:text/plain;UTF-8,{data}"
            return f"{grammar_selected}", data
        return '', ''

    @app.callback(
        [
            Output('grammar-input', 'value'),
            Output('grammar-text-area', 'value'),
            Output('grammar-input', 'disabled'),
            Output('grammar-btn-add', 'style'),
            Output('grammar-btn-update', 'style')
        
        ],
        [
            Input('grammar-dropdown', 'value'),
            Input('grammar-dropdown', 'options'),
            Input('store-grammar', 'data')
        ]
    )
    def select_grammar(grammar_selected, grammar_options, grammar_data):
        if grammar_options:
            keys = [v['value'] for v in grammar_options]
            if grammar_selected in keys:
                grammar_text = tomato_gram.obj_para_texto(grammar_data[grammar_selected])
                return grammar_selected, grammar_text, True, {'display': 'none'}, {}
        return "", "", False, {}, {'display': 'none'}


    @app.callback(
        Output('grammar-dropdown', 'options'),
        [
            Input('store-grammar', 'data'),
        ],
    )
    def update_options(grammar_data):
        options = [{'label': k, 'value': k} for k in grammar_data.keys()]
        return options


    @app.callback(
        [
            Output('store-grammar', 'data'),
            Output('grammar-alert', 'children'),
        ],
        [
            Input('grammar-upload','contents'),
            Input('grammar-upload', 'filename'),
            Input('grammar-btn-add', 'n_clicks'),
            Input('grammar-btn-update', 'n_clicks'),
            Input('grammar-btn-rm', 'n_clicks'),
        ],
        [
            State('grammar-dropdown', 'value'),
            State('grammar-dropdown', 'options'),
            State('grammar-input', 'value'),
            State('grammar-text-area', 'value'),
            State('store-grammar', 'data')
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
        ctx = dash.callback_context
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if triggered_id == 'grammar-upload' or triggered_id == 'grammar-filename':
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
                    grammar_obj = tomato_gram.texto_para_obj(decoded_content, grammar_id)
                    grammar_data[grammar_id] = grammar_obj

                alert = dbc.Alert(alert_text, color=alert_type, duration=4000)
                return grammar_data, alert

        elif triggered_id == 'grammar-btn-add' and grammar_name:
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

            alert = dbc.Alert(alert_text, color=alert_type, duration=4000)
            return grammar_data, alert

        elif triggered_id == 'grammar-btn-update' and grammar_selected:
            grammar_obj = tomato_gram.texto_para_obj(grammar_text, grammar_selected)
            grammar_data[grammar_selected] = grammar_obj

            alert_text = f"Gramática '{grammar_selected}' atualizada com sucesso :)"
            alert_type = "success" 
            alert = dbc.Alert(alert_text, color=alert_type, duration=4000)
            return grammar_data, alert 

        elif triggered_id == 'grammar-btn-rm' and grammar_selected:
            grammar_data.pop(grammar_selected, None)
            alert_text = f"Gramática '{grammar_selected}' deletada com sucesso :)"
            alert_type = "success" 
            alert = dbc.Alert(alert_text, color=alert_type, duration=4000)
            return grammar_data, alert

        return grammar_data, []

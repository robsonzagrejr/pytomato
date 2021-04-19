import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import base64

import pytomato.expressao_regular as tomato_er
import pages.lexical_an.data as d


"""Funções de Callback

Funções que definem as triggers e execução de cada callback.
"""
def register_callbacks(app):
    @app.callback(
        Output("lexical-an-token-modal", "is_open"),
        [
            Input("lexical-an-btn-modal-open", "n_clicks"),
        ],
        [
            State("lexical-an-token-modal", "is_open")
        ],
    )
    def toggle_modal(n, is_open):
        if n:
            return not is_open
        return is_open


    @app.callback(
        [
            Output('lexical-an-download','download'),
            Output('lexical-an-download', 'href'),
        ],
        [
            Input('lexical-an-dropdown', 'value'),
            Input('store-lexical-an', 'data'),
        ],
    )
    def lexical_an_download(lexical_an_selected, lexical_an_data):
        """Callback Download Expressão Regular

        Callback para chamada de download de expressão regular
        em arquivo de texto.
        """
     
        if lexical_an_selected and lexical_an_selected in lexical_an_data.keys():
            data = tomato_er.obj_para_texto(lexical_an_data[lexical_an_selected])
            data = data.replace('\n', "%0D%0A");
            data = f"data:text/plain;UTF-8,{data}"
            return f"{lexical_an_selected}", data
        return '', ''

    @app.callback(
        [
            Output('lexical-an-input', 'value'),
            Output('lexical-an-text-area', 'value'),
            Output('lexical-an-input', 'disabled'),
            Output('lexical-an-btn-add', 'style'),
            Output('lexical-an-btn-update', 'style')
        
        ],
        [
            Input('lexical-an-dropdown', 'value'),
            Input('lexical-an-dropdown', 'options'),
            Input('store-lexical-an', 'data')
        ]
    )
    def select_lexical_an(lexical_an_selected, lexical_an_options, lexical_an_data):
        """Callback Seleção Expressão Regular

        Callback para gerenciar a seleção e display do
        dropdown das expressões regulares.
        """
    
        if lexical_an_options:
            keys = [v['value'] for v in lexical_an_options]
            if lexical_an_selected in keys:
                lexical_an_text = tomato_er.obj_para_texto(lexical_an_data[lexical_an_selected])
                return lexical_an_selected, lexical_an_text, True, {'display': 'none'}, {}
        return "", "", False, {}, {'display': 'none'}


    @app.callback(
        Output('lexical-an-dropdown', 'options'),
        [
            Input('store-lexical-an', 'data'),
        ],
    )
    def update_options(lexical_an_data):
        options = [{'label': k, 'value': k} for k in lexical_an_data.keys()]
        return options


    @app.callback(
        [
            Output('store-lexical-an-helper', 'data'),
            Output('lexical-an-alert', 'children'),
        ],
        [
            Input('lexical-an-upload','contents'),
            Input('lexical-an-upload', 'filename'),
            Input('lexical-an-btn-add', 'n_clicks'),
            Input('lexical-an-btn-update', 'n_clicks'),
            Input('lexical-an-btn-rm', 'n_clicks'),
        ],
        [
            State('lexical-an-dropdown', 'value'),
            State('lexical-an-dropdown', 'options'),
            State('lexical-an-input', 'value'),
            State('lexical-an-text-area', 'value'),
            State('store-lexical-an', 'data'),
            State('store-automaton', 'data'),
        ]
    )
    def update_lexical_an_data(
            file_content,
            file_name,
            add_click,
            update_click,
            rm_click,

            lexical_an_selected,
            lexical_an_options,
            lexical_an_name,
            lexical_an_text,
            lexical_an_data,
            automaton_data,
        ):
        """Callback Update Expressão Regular

        Callback que gerencia criação, exclusão, upload, alteração
        de expressão regular
        """
    
        ctx = dash.callback_context
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if triggered_id == 'lexical-an-upload' or triggered_id == 'lexical-an-filename':
            if file_name:
                lexical_an_data, alert = d.upload_lexical_an(
                    file_name,
                    file_content,
                    lexical_an_options,
                    lexical_an_data
                )
                return lexical_an_data, alert

        elif triggered_id == 'lexical-an-btn-add' and lexical_an_name:
            lexical_an_data, alert = d.add_lexical_an(
                lexical_an_name,
                lexical_an_text,
                lexical_an_options,
                lexical_an_data
            )
            return lexical_an_data, alert

        elif triggered_id == 'lexical-an-btn-update' and lexical_an_selected:
            lexical_an_data, alert = d.update_lexical_an(
                lexical_an_text,
                lexical_an_selected,
                lexical_an_data
            )
            return lexical_an_data, alert 

        elif triggered_id == 'lexical-an-btn-rm' and lexical_an_selected:
            lexical_an_data, alert = d.remove_lexical_an(
                lexical_an_selected,
                lexical_an_data
            )
            return lexical_an_data, alert


        return lexical_an_data, []


    #Conversoes
    @app.callback(
        Output('store-lexical-an', 'data'),
        [
            Input('store-lexical-an-helper', 'data'),
        ],
        [
            State('store-lexical-an', 'data')
        ]
    )
    def lexical_an_data(lexical_an_data_helper, lexical_an_data):
        """Callback Download Expressão Regular

        """
        if 'type' not in lexical_an_data_helper.keys():
            return lexical_an_data_helper
     
        return lexical_an_data


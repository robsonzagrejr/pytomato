import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import base64

import pytomato.gramatica as tomato_gram
import pages.grammar.data as d

"""Funções de Callback

Funções que definem as triggers e execução de cada callback.
"""
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
        """Callback Download Gramática

        Callback para chamada de download de gramáticas
        em arquivo de texto.
        """
     
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
        """Callback Seleção Gramática

        Callback para gerenciar a seleção e display do
        dropdown das gramáticas.
        """
    
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
            Output('store-grammar-helper', 'data'),
            Output('grammar-alert', 'children'),
        ],
        [
            Input('grammar-upload','contents'),
            Input('grammar-upload', 'filename'),
            Input('grammar-btn-add', 'n_clicks'),
            Input('grammar-btn-update', 'n_clicks'),
            Input('grammar-btn-rm', 'n_clicks'),
            Input('grammar-btn-convert-af', 'n_clicks'),
        ],
        [
            State('grammar-dropdown', 'value'),
            State('grammar-dropdown', 'options'),
            State('grammar-input', 'value'),
            State('grammar-text-area', 'value'),
            State('store-grammar', 'data'),
            State('store-automaton', 'data'),
        ]
    )
    def update_grammar_data(
            file_content,
            file_name,
            add_click,
            update_click,
            rm_click,
            gr_convert_af_click,

            grammar_selected,
            grammar_options,
            grammar_name,
            grammar_text,
            grammar_data,
            automaton_data,
        ):
        """Callback Update Gramática

        Callback que gerencia criação, exclusão, upload, alteração
        de gramática.
        """
    
        ctx = dash.callback_context
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if triggered_id == 'grammar-upload' or triggered_id == 'grammar-filename':
            if file_name:
                grammar_data, alert = d.upload_grammar(
                    file_name,
                    file_content,
                    grammar_options,
                    grammar_data
                )
                return grammar_data, alert

        elif triggered_id == 'grammar-btn-add' and grammar_name:
            grammar_data, alert = d.add_grammar(
                grammar_name,
                grammar_text,
                grammar_options,
                grammar_data
            )

            return grammar_data, alert

        elif triggered_id == 'grammar-btn-update' and grammar_selected:
            grammar_data, alert = d.update_grammar(
                grammar_text,
                grammar_selected,
                grammar_data
            )
            return grammar_data, alert 

        elif triggered_id == 'grammar-btn-rm' and grammar_selected:
            grammar_data, alert = d.remove_grammar(
                grammar_selected,
                grammar_data
            )
            return grammar_data, alert

        elif (triggered_id == 'grammar-btn-convert-af' and
             grammar_selected and grammar_selected in grammar_data.keys()):

            helper_data, alert = d.convert_grammar_to_af(
                grammar_selected,
                grammar_data,
                automaton_data
            ) 
            return helper_data, alert

        return grammar_data, []


    #Conversoes
    @app.callback(
        Output('store-grammar', 'data'),
        [
            Input('store-grammar-helper', 'data'),
        ],
        [
            State('store-grammar', 'data')
        ]
    )
    def grammar_data(grammar_data_helper, grammar_data):
        """Callback Download Gramática

        """
        if 'type' not in grammar_data_helper.keys():
            return grammar_data_helper
     
        return grammar_data


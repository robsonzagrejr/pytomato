import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import base64

import pytomato.gramatica as tomato_gram
import pages.sintatic_an.data as d

"""Funções de Callback

Funções que definem as triggers e execução de cada callback.
"""
def register_callbacks(app):
    @app.callback(
        [
            Output('sintatic-an-download','download'),
            Output('sintatic-an-download', 'href'),
        ],
        [
            Input('sintatic-an-dropdown', 'value'),
            Input('store-sintatic-an', 'data'),
        ],
    )
    def sintatic_an_download(sintatic_an_selected, sintatic_an_data):
        """Callback Download Gramática

        Callback para chamada de download de gramáticas
        em arquivo de texto.
        """
     
        if sintatic_an_selected and sintatic_an_selected in sintatic_an_data.keys():
            data = tomato_gram.obj_para_texto(sintatic_an_data[sintatic_an_selected])
            data = data.replace('\n', "%0D%0A");
            data = f"data:text/plain;UTF-8,{data}"
            return f"{sintatic_an_selected}", data
        return '', ''

    @app.callback(
        [
            Output('sintatic-an-input', 'value'),
            Output('sintatic-an-text-area', 'value'),
            Output('sintatic-an-input', 'disabled'),
            Output('sintatic-an-btn-add', 'style'),
            Output('sintatic-an-btn-update', 'style')
        
        ],
        [
            Input('sintatic-an-dropdown', 'value'),
            Input('sintatic-an-dropdown', 'options'),
            Input('store-sintatic-an', 'data')
        ]
    )
    def select_sintatic_an(sintatic_an_selected, sintatic_an_options,
            sintatic_an_data):
        """Callback Seleção Gramática

        Callback para gerenciar a seleção e display do
        dropdown das gramáticas.
        """
    
        if sintatic_an_options:
            keys = [v['value'] for v in sintatic_an_options]
            if sintatic_an_selected in keys:
                sintatic_an_text = tomato_gram.obj_para_texto(sintatic_an_data[sintatic_an_selected])
                return sintatic_an_selected, sintatic_an_text, True, {'display': 'none'}, {}
        return "", "", False, {}, {'display': 'none'}


    @app.callback(
        Output('sintatic-an-dropdown', 'options'),
        [
            Input('store-sintatic-an', 'data'),
        ],
    )
    def update_options(sintatic_an_data):
        options = [{'label': k, 'value': k} for k in sintatic_an_data.keys()]
        return options


    @app.callback(
        [
            Output('sintatic-an-items-div', 'children'),
            Output('sintatic-an-table', 'columns'),
            Output('sintatic-an-table', 'data'),
        ],
        [
            Input('sintatic-an-dropdown', 'value'),
            Input('store-sintatic-an', 'data'),
        ],
    )
    def update_items(sintatic_an_selected, sintatic_an_data):
        if sintatic_an_selected in sintatic_an_data.keys():
            print('ALGO')
            return d.print_items_table(sintatic_an_selected, sintatic_an_data)
        print("LALAL")
        return '',[],[]




    @app.callback(
        [
            Output('store-sintatic-an-helper', 'data'),
            Output('sintatic-an-alert', 'children'),
        ],
        [
            Input('sintatic-an-upload','contents'),
            Input('sintatic-an-upload', 'filename'),
            Input('sintatic-an-btn-add', 'n_clicks'),
            Input('sintatic-an-btn-update', 'n_clicks'),
            Input('sintatic-an-btn-rm', 'n_clicks'),
            Input('sintatic-an-btn-convert-af', 'n_clicks'),
        ],
        [
            State('sintatic-an-dropdown', 'value'),
            State('sintatic-an-dropdown', 'options'),
            State('sintatic-an-input', 'value'),
            State('sintatic-an-text-area', 'value'),
            State('store-sintatic-an', 'data'),
            State('store-automaton', 'data'),
        ]
    )
    def update_sintatic_an_data(
            file_content,
            file_name,
            add_click,
            update_click,
            rm_click,
            gr_convert_af_click,

            sintatic_an_selected,
            sintatic_an_options,
            sintatic_an_name,
            sintatic_an_text,
            sintatic_an_data,
            automaton_data,
        ):
        """Callback Update Gramática

        Callback que gerencia criação, exclusão, upload, alteração
        de gramática.
        """
    
        ctx = dash.callback_context
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if triggered_id == 'sintatic-an-upload' or triggered_id == 'sintatic-an-filename':
            if file_name:
                sintatic_an_data, alert = d.upload_sintatic_an(
                    file_name,
                    file_content,
                    sintatic_an_options,
                    sintatic_an_data
                )
                return sintatic_an_data, alert

        elif triggered_id == 'sintatic-an-btn-add' and sintatic_an_name:
            sintatic_an_data, alert = d.add_sintatic_an(
                sintatic_an_name,
                sintatic_an_text,
                sintatic_an_options,
                sintatic_an_data
            )

            return sintatic_an_data, alert

        elif triggered_id == 'sintatic-an-btn-update' and sintatic_an_selected:
            sintatic_an_data, alert = d.update_sintatic_an(
                sintatic_an_text,
                sintatic_an_selected,
                sintatic_an_data
            )
            return sintatic_an_data, alert 

        elif triggered_id == 'sintatic-an-btn-rm' and sintatic_an_selected:
            sintatic_an_data, alert = d.remove_sintatic_an(
                sintatic_an_selected,
                sintatic_an_data
            )
            return sintatic_an_data, alert

        return sintatic_an_data, []


    #Conversoes
    @app.callback(
        Output('store-sintatic-an', 'data'),
        [
            Input('store-sintatic-an-helper', 'data'),
            Input('store-automaton-helper', 'data'),
        ],
        [
            State('store-sintatic-an', 'data')
        ]
    )
    def sintatic_an_data(sintatic_an_data_helper, automaton_data_helper,
            sintatic_an_data):
        """Callback Download Gramática

        """
        ctx = dash.callback_context
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if triggered_id == 'store-sintatic-an-helper':
            if 'type' not in sintatic_an_data_helper.keys():
                return sintatic_an_data_helper

        elif triggered_id == 'store-automaton-helper' and 'type' in automaton_data_helper.keys():
            if automaton_data_helper['type'] == 'GR':
                sintatic_an_name = automaton_data_helper['name']
                sintatic_an_obj = automaton_data_helper['data']
                sintatic_an_data[sintatic_an_name] = sintatic_an_obj
                return sintatic_an_data
     
        return sintatic_an_data


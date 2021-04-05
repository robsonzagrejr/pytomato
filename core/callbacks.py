import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State

# Importe das funções de backend.
import pages.grammar as grammar
import pages.automaton as automaton
import pages.regular_exp as regular_exp

import pytomato as tomato

"""Callbacks para Páginas

Define os callbacks(inputs/outputs/states) para cada
página, Gramática e Autômato.
"""
def register_callbacks(app):

    @app.callback(
        Output('page-content', 'children'),
        [
            Input('url', 'pathname')
        ]
    )
    def display_page(pathname):
        base = '/'
        if app.config['url_base_pathname'] is not None:
            base = app.config['url_base_pathname']

        if pathname == base or pathname == f'{base}grammar':
            return grammar.layout

        elif pathname == f'{base}automaton':
            return automaton.layout

        elif pathname == f'{base}regular_exp':
            return regular_exp.layout
        

    grammar.register_callbacks(app)
    automaton.register_callbacks(app)
    regular_exp.register_callbacks(app)


    """Callback que irá lidar com conversões entre tipos
    """
    """
    @app.callback(
        Output('store-convertion-helper', 'data'),
        [
            Input('grammar-btn-convert-af', 'n_clicks'),
            Input('regular-exp-btn-convert-af', 'n_clicks'),
        ],
        [
            State('store-grammar', 'data'),
            State('store-automaton', 'data'),
            State('store-regular-exp', 'data'),
        ]
    )
    def display_page(
        btn_grammar_automaton,
        btn_regular_exp_automaton,
        grammar_data, 
        automaton_data,
        regular_exp_data
        ):
        ctx = dash.callback_context
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if triggered_id == 'grammar-btn-convert-af':
            print('conversao de Gramatica para AF')
        elif triggered_id == 'regular-exp-btn-convert-af':
            print('conversao de ER para AF')

        raise PreventUpdate
    """
     

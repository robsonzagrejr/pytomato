import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State

# Importe das funções de backend.
import pages.grammar as grammar
import pages.automaton as automaton
import pages.regular_exp as regular_exp
import pages.lexical_an as lexical_an 
import pages.sintatic_an as sintatic_an 

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

        elif pathname == f'{base}lexical_an':
            return lexical_an.layout
        
        elif pathname == f'{base}sintatic_an':
            return sintatic_an.layout
        

    grammar.register_callbacks(app)
    automaton.register_callbacks(app)
    regular_exp.register_callbacks(app)
    lexical_an.register_callbacks(app)
    sintatic_an.register_callbacks(app)


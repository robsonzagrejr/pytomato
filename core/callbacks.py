from dash import callback_context
from dash.dependencies import Input, Output, State

# Importe das funções de backend.
import pages.grammar as grammar
import pages.automaton as automaton
import pages.regular_exp as regular_exp

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

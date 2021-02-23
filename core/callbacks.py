from dash import callback_context
from dash.dependencies import Input, Output, State

import pages.grammar as grammar
import pages.automaton as automaton
# registra os callbacks no app que fazer a interface de entrada/saida com nosso código python
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
        

    grammar.register_callbacks(app)
    automaton.register_callbacks(app)

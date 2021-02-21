from dash import callback_context
from dash.dependencies import Input, Output, State

def register_callbacks(app):

    @app.callback(
        [
            Output('', 'children'),
        ],
        [
        Input('url', 'pathname')
        ]
    )
    def display_page(pathname):
        pass


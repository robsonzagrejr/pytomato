import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State

import pytomato.gramatica as tomato_gram

def register_callbacks(app):

    @app.callback(
        [
            Output('grammar-input', 'value'),
            Output('grammar-text-area', 'value'),
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
                grammar_text = tomato_gram.retornar_gramatica(grammar_data[grammar_selected])
                return grammar_selected, grammar_text
        return "", ""


    @app.callback(
        Output('grammar-dropdown', 'options'),
        [
            Input('store-grammar', 'data')
        ],
    )
    def select_grammar(grammar_data):
        options = [{'label': k, 'value': k} for k in grammar_data.keys()]
        return options


    @app.callback(
        [
            Output('grammar-input', 'disabled'),
            Output('grammar-btn-add', 'style'),
            Output('grammar-btn-update', 'style')
        ],
        [
            Input('grammar-input', 'value')
        ],
        [
            State('grammar-dropdown', 'options')
        ]
    )
    def select_grammar(grammar_name, grammar_options):
        if grammar_name and grammar_options:
            existing_names = [g['value'] for g in grammar_options]

            if grammar_name in existing_names:
                return True, {'display': 'none'}, {}
        return False, {}, {'display': 'none'}


    @app.callback(
        Output('store-grammar', 'data'),
        [
            Input('grammar-btn-add', 'n_clicks'),
            Input('grammar-btn-update', 'n_clicks'),
            Input('grammar-btn-rm', 'n_clicks'),
        ],
        [
            State('grammar-dropdown', 'value'),
            State('grammar-input', 'value'),
            State('grammar-text-area', 'value'),
            State('store-grammar', 'data')
        ]
    )
    def select_grammar(add_click, update_click, rm_click, grammar_selected,  grammar_name, grammar_text, grammar_data):
        ctx = dash.callback_context
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if not ctx.triggered:
            raise PreventUpdate

        if triggered_id == 'grammar-btn-add' and grammar_name:
            grammar_id = grammar_name.replace(' ','_').lower()
            grammar_obj = tomato_gram.traduzir_gramatica(grammar_text, grammar_id)
            grammar_data[grammar_id] = grammar_obj
            return grammar_data

        elif triggered_id == 'grammar-btn-update' and grammar_selected:
            grammar_obj = tomato_gram.traduzir_gramatica(grammar_text, grammar_id)
            grammar_data[grammar_selected] = grammar_obj
            return grammar_data

        elif triggered_id == 'grammar-btn-rm' and grammar_selected:
            grammar_data.pop(grammar_selected, None)
            return grammar_data

        raise PreventUpdate

    

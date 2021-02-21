import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

import pytomato.automato as tomato_gram

def register_callbacks(app):

    @app.callback(
        [
            Output('automaton-input', 'value'),
            Output('automaton-text-area', 'value'),
            Output('automaton-input', 'disabled'),
            Output('automaton-btn-add', 'style'),
            Output('automaton-btn-update', 'style')
        
        ],
        [
            Input('automaton-dropdown', 'value'),
            Input('automaton-dropdown', 'options'),
            Input('store-automaton', 'data')
        ]
    )
    def select_automaton(automaton_selected, automaton_options, automaton_data):
        if automaton_options:
            keys = [v['value'] for v in automaton_options]
            if automaton_selected in keys:
                automaton_text
                = tomato_gram.retornar_gramatica(automaton_data[automaton_selected])
                return automaton_selected, automaton_text, True, {'display': 'none'}, {}
        return "", "", False, {}, {'display': 'none'}


    @app.callback(
        Output('automaton-dropdown', 'options'),
        [
            Input('store-automaton', 'data'),
        ],
    )
    def update_options(automaton_data):
        options = [{'label': k, 'value': k} for k in automaton_data.keys()]
        return options


    @app.callback(
        [
            Output('store-automaton', 'data'),
            Output('automaton-alert', 'children'),
        ],
        [
            Input('automaton-btn-add', 'n_clicks'),
            Input('automaton-btn-update', 'n_clicks'),
            Input('automaton-btn-rm', 'n_clicks'),
        ],
        [
            State('automaton-dropdown', 'value'),
            State('automaton-dropdown', 'options'),
            State('automaton-input', 'value'),
            State('automaton-text-area', 'value'),
            State('store-automaton', 'data')
        ]
    )
    def update_automaton_data(
            add_click,
            update_click,
            rm_click,
            automaton_selected,
            automaton_options,
            automaton_name,
            automaton_text,
            automaton_data
        ):
        ctx = dash.callback_context
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if triggered_id == 'automaton-btn-add' and automaton_name:
            automaton_id = automaton_name.replace(' ','_').lower()

            alert_text = f'Gramática {automaton_name} adicionada com sucesso :D'
            alert_type = 'success'
            keys = [v['value'] for v in automaton_options]
            if automaton_id in keys:
                alert_text = f"Gramática '{automaton_name}' já existe :X"
                alert_type = 'danger'
            else:
                automaton_obj = tomato_gram.traduzir_gramatica(automaton_text,
                        automaton_id)
                automaton_data[automaton_id] = automaton_obj

            alert = dbc.Alert(alert_text, color=alert_type, duration=4000)
            return automaton_data, alert

        elif triggered_id == 'automaton-btn-update' and automaton_selected:
            automaton_obj = tomato_gram.traduzir_gramatica(automaton_text,
                    automaton_selected)
            automaton_data[automaton_selected] = automaton_obj

            alert_text = f"Gramática '{automaton_selected}' atualizada com sucesso :)"
            alert_type = "success" 
            alert = dbc.Alert(alert_text, color=alert_type, duration=4000)
            return automaton_data, alert 

        elif triggered_id == 'automaton-btn-rm' and automaton_selected:
            automaton_data.pop(automaton_selected, None)
            alert_text = f"Gramática '{automaton_selected}' deletada com sucesso :)"
            alert_type = "success" 
            alert = dbc.Alert(alert_text, color=alert_type, duration=4000)
            return automaton_data, alert

        return automaton_data, []

    

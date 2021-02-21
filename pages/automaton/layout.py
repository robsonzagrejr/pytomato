
import dash_bootstrap_components as dbc
import dash_html_components as html

from .components import (
    widgets
)

inputs = dbc.Container(
    children=[
        html.Br(),
        html.Br(),
        dbc.Row(
            html.H3('Automato'),
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        widgets['grammar_text_area'],
                    ],
                    md=6,
                ),
                dbc.Col(
                    [
                        widgets['grammar_table'],
                    ],
                    md=6,
                ),
            ]
        ),
    ]
)


outputs = dbc.Container(
    children=[
        html.Br(),
        html.Hr(),
        dbc.Row(html.H3('Automato')),
        dbc.Row(
            [
                dbc.Col(
                    [
                        #widgets['automaton_table'],
                    ],
                    md=12,
                ),
            ]
        )
    ]
)

layout = [
    inputs,
    outputs
]

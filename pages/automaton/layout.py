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
            html.H1('Automato'),
        ),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label('Selecione o Automato:'),
                        widgets['automaton_dropdown'],
                    ],
                    md=3
                ),
                dbc.Col(
                    [
                        widgets['automaton_download'],
                    ],
                    md=1,
                ),
                dbc.Col(
                    [
                        widgets['automaton_upload'],
                    ],
                    md=1,
                ),
            ],
            align="end",
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label('Nome:'),
                        widgets['automaton_input'],
                    ],
                    md=3
                ),
                dbc.Col(
                    [
                        widgets['automaton_btn_add'],
                        widgets['automaton_btn_update'],
                        widgets['automaton_btn_rm'],
                    ],
                    md=6,
                ),
            ],
            align="end",
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label('Automato:'),
                        widgets['automaton_text_area'],
                    ],
                    md=7,
                ),
            ]
        ),
        html.Br(),
        widgets['automaton_alert'],
        ]
)


outputs = dbc.Container(
    children=[
        html.Br(),
        html.Hr(),
        widgets['automaton_table'],
        html.Br(),
        html.Br(),
    ]
)

layout = [
    inputs,
    outputs
]

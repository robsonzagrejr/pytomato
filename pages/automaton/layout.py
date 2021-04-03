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
                dbc.Col(
                    [
                        html.Br(),
                        html.Label("n_de_estados"),
                        html.Br(),
                        html.Label("estado_inicial"),
                        html.Br(),
                        html.Label("estados_de_aceitacao"),
                        html.Br(),
                        html.Label("alfabeto"),
                        html.Br(),
                        html.Label("transicao_1"),
                        html.Br(),
                        html.Label("transicao_2"),
                        html.Br(),
                        html.Label("."),
                        html.Br(),
                        html.Label("."),
                        html.Br(),
                        html.Label("transicao_n"),
                    ]
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
        widgets['automaton_btn_update_from_table'],
        widgets['automaton_table'],
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
    ]
)

layout = [
    inputs,
    outputs
]

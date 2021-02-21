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
            html.H1('Gramática'),
        ),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label('Selecione a Gramática:'),
                        widgets['grammar_dropdown'],
                    ],
                    md=7
                )
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label('Nome:'),
                        widgets['grammar_input'],
                    ],
                    md=3
                ),
                dbc.Col(
                    [
                        widgets['grammar_btn_add'],
                        widgets['grammar_btn_update'],
                        widgets['grammar_btn_rm'],
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
                        html.Label('Gramática:'),
                        widgets['grammar_text_area'],
                    ],
                    md=7,
                ),
            ]
        ),
        ]
)


outputs = dbc.Container(
    children=[
        html.Br(),
        html.Hr(),
        html.Div(id='dict-store'),
    ]
)

layout = [
    inputs,
    outputs
]

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
            html.H1('Análise Sintática'),
        ),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label('Selecione a GLC:'),
                        widgets['sintatic_an_dropdown'],
                    ],
                    md=3
                ),
                dbc.Col(
                    [
                        widgets['sintatic_an_download'],
                    ],
                    md=1,
                ),
                dbc.Col(
                    [
                        widgets['sintatic_an_upload'],
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
                        widgets['sintatic_an_input'],
                    ],
                    md=3
                ),
                dbc.Col(
                    [
                        widgets['sintatic_an_btn_add'],
                        widgets['sintatic_an_btn_update'],
                        widgets['sintatic_an_btn_rm'],
                        widgets['sintatic_an_btn_convert_af'],
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
                        widgets['sintatic_an_text_area'],
                    ],
                    md=7,
                ),
            ]
        ),
        html.Br(),
        widgets['sintatic_an_alert'],
        ]
)


outputs = dbc.Container(
    children=[
        html.Br(),
        html.Hr(),
    ]
)

layout = [
    inputs,
    outputs
]

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
            html.H1('Expressão Regular'),
        ),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label('Selecione uma Expressão Regular:'),
                        widgets['regular_exp_dropdown'],
                    ],
                    md=3
                ),
                dbc.Col(
                    [
                        widgets['regular_exp_download'],
                    ],
                    md=1,
                ),
                dbc.Col(
                    [
                        widgets['regular_exp_upload'],
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
                        widgets['regular_exp_input'],
                    ],
                    md=3
                ),
                dbc.Col(
                    [
                        widgets['regular_exp_btn_add'],
                        widgets['regular_exp_btn_update'],
                        widgets['regular_exp_btn_rm'],
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
                        html.Label('Expressão Regular:'),
                        widgets['regular_exp_text_area'],
                    ],
                    md=7,
                ),
            ]
        ),
        html.Br(),
        widgets['regular_exp_alert'],
        ]
)


outputs = dbc.Container(
    children=[
        html.Br(),
        html.Hr(),
        #widgets['regular_exp_btn_update_from_table'],
        #widgets['regular_exp_table'],
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

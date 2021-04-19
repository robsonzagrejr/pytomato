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
            html.H1('Análise Léxica'),
        ),
        html.Br(),
        html.Br(),
        
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label('Selecione uma "Linguagem":'),
                        widgets['lexical_an_dropdown'],
                    ],
                    md=3
                ),
                dbc.Col(
                    [
                        widgets['lexical_an_btn_modal_open'],
                    ],
                    md=1,
                ),

                dbc.Col(
                    [
                        widgets['lexical_an_download'],
                    ],
                    md=1,
                ),
                dbc.Col(
                    [
                        widgets['lexical_an_upload'],
                    ],
                    md=1,
                ),
            ],
            align="end",
        ),
        html.Br(),
        dbc.Modal(
            [
                dbc.ModalHeader("Definição de Tokens"),
                dbc.ModalBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Label('Linguagem:'),
                                        widgets['lexical_an_input'],
                                    ],
                                    md=6
                                ),
                                dbc.Col(
                                    [
                                        widgets['lexical_an_btn_add'],
                                        widgets['lexical_an_btn_update'],
                                        widgets['lexical_an_btn_rm'],
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
                                        html.Label('Tokens:'),
                                    ],
                                    md=12,
                                ),
                            ],
                            align="end",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        widgets['lexical_an_text_area'],
                                    ],
                                    md=12,
                                ),
                            ]
                        ),
                    ]
                ),
                dbc.ModalFooter(
                ),
            ],
            id="lexical-an-token-modal",
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label('Digite o Pseudo Código'),
                        widgets['lexical_an_pseudo_cod_ta'],
                    ],
                    md=6,
                ),
                dbc.Col(
                    [
                        html.Br(),
                        widgets['lexical_an_table'],
                    ],
                    md=6,
                ),
                
            ]
        ),
        html.Br(),
        widgets['lexical_an_alert'],
        ]
)


outputs = dbc.Container(
    children=[
        html.Br(),
        html.Hr(),
        #widgets['lexical_an_btn_update_from_table'],
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

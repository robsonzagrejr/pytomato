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
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Label('Selecione o Automato:'),
                                        widgets['automaton_dropdown'],
                                    ],
                                    md=6
                                ),
                                dbc.Col(
                                    [
                                        widgets['automaton_download'],
                                    ],
                                    md=2,
                                ),
                                dbc.Col(
                                    [
                                        widgets['automaton_upload'],
                                    ],
                                    md=2,
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
                                    md=6
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
                    ]
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Label('Operação:'),
                                        widgets['automaton_operation_dropdown']
                                    ],
                                    md=6
                                ),
                            ],
                            align="end",
                        ),
                        html.Br(),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Label('Segundo Automato:'),
                                        widgets['automaton_second_dropdown']
                                    ],
                                    md=6
                                ),
                                dbc.Col(
                                    [
                                        widgets['automaton_btn_convert_gr'],
                                        widgets['automaton_btn_apply_operation']
                                    ],
                                    md=6
                                ),

                            ],
                            align="end",
                        ),
                    ]
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
                    md=6,
                ),
                dbc.Col(
                    [
                        widgets['automaton_btn_collapse_tip'],
                        dbc.Popover(
                            [
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
                                html.Label("..."),
                                html.Br(),
                                html.Label("transicao_n"),
                            ],
                            id='automaton-collapse-tip',
                            target="automaton-text-area",
                            placement='left',
                        ),
                        widgets['automaton_graph'],
                    ],
                ),
            ]
        ),
        html.Br(),
        widgets['automaton_alert'],
    ]
)


outputs = dbc.Container(
    children=[
        html.Hr(),
        widgets['automaton_btn_update_from_table'],
        widgets['automaton_table'],
        html.Br(),
        html.Br(),
        html.Br(),
    ]
)

layout = [
    inputs,
    outputs
]

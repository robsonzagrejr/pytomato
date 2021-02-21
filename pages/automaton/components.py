import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash_table import DataTable


widgets = {
    'automaton_dropdown': dcc.Dropdown(
        id='automaton-dropdown',
    ),
    'automaton_input': dbc.Input(
        id='automaton-input',
        placeholder='Gramatica label',
    ),
    'automaton_text_area': dbc.Textarea(
        id='automaton-text-area',
        placeholder="Digite a Gramática"
    ),
    'automaton_btn_add': dbc.Button(
        "Adicionar",
        id='automaton-btn-add',
        color='dark',
        outline=True,
        className='btn',
    ),
    'automaton_btn_update': dbc.Button(
        "Atualizar",
        id='automaton-btn-update',
        color='secondary',
        outline=True,
        className='btn',
        style={'display': 'none'},
    ),
    'automaton_btn_rm': dbc.Button(
        "Remover",
        id='automaton-btn-rm',
        color='danger',
        outline=True,
        className='btn',
    ),
    'automaton_alert': html.Div(
        id='automaton-alert',
    ),
    'automaton_table': DataTable(
        id='automaton-table',
        columns=[
            {'name':'nonterminal','id':'nonterminal'},
            {'name':'first set','id':'first set',},
            {'name':'follow set','id':'follow set',},
            {'name':'nullable','id':'nullable',},
            {'name':'endable','id':'endable',},
        ],
        data = [
            {'nonterminal':'S'},
        ],
        editable=False,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        page_action="native",
        page_current=0,
        page_size=10,
        style_table={
            'overflow': 'auto',
            'margin': '0 15px 0 15px',
        },
    ),
}


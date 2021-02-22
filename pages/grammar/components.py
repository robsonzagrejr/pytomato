import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash_table import DataTable


widgets = {
    'grammar_dropdown': dcc.Dropdown(
        id='grammar-dropdown',
    ),
    'grammar_input': dbc.Input(
        id='grammar-input',
        placeholder='Gramatica label',
    ),
    'grammar_text_area': dbc.Textarea(
        id='grammar-text-area',
        placeholder="Digite a Gramática",
        className='bigarea',
    ),
    'grammar_btn_add': dbc.Button(
        "Adicionar",
        id='grammar-btn-add',
        color='dark',
        outline=True,
        className='btn-margin',
    ),
    'grammar_btn_update': dbc.Button(
        "Atualizar",
        id='grammar-btn-update',
        color='secondary',
        outline=True,
        className='btn-margin',
        style={'display': 'none'},
    ),
    'grammar_btn_rm': dbc.Button(
        "Remover",
        id='grammar-btn-rm',
        color='danger',
        outline=True,
        className='btn-margin',
    ),
    'grammar_alert': html.Div(
        id='grammar-alert',
    ),
    'grammar_upload': dcc.Upload(
        id='grammar-upload',
        children=html.Div([
            html.A('Upload')
        ]),
        multiple=False,
       className='btn btn-margin btn-outline-dark'
    ),
    'grammar_download': html.A(
        "Dowload",
        id='grammar-download',
        className='btn btn-margin btn-outline-dark'
    ),
    'grammar_table': DataTable(
        id='grammar-table',
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


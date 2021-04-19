import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash_table import DataTable


widgets = {
    'lexical_an_dropdown': dcc.Dropdown(
        id='lexical-an-dropdown',
    ),
    'lexical_an_label': dbc.Label(
        id='lexical-an-label',
        #placeholder='Linguagem label',
    ),
    'lexical_an_input': dbc.Input(
        id='lexical-an-input',
        placeholder='Linguagem label',
    ),
    'lexical_an_text_area': dbc.Textarea(
        id='lexical-an-text-area',
        placeholder="Digite a ER definindo os Tokens",
        className='bigarea',
    ),
    'lexical_an_btn_modal_open': dbc.Button(
        "+",
        id='lexical-an-btn-modal-open',
        color='dark',
        outline=True,
        className='btn-margin',
    ),

    'lexical_an_btn_add': dbc.Button(
        "Adicionar",
        id='lexical-an-btn-add',
        color='dark',
        outline=True,
        className='btn-margin',
    ),
    'lexical_an_btn_update': dbc.Button(
        "Atualizar",
        id='lexical-an-btn-update',
        color='secondary',
        outline=True,
        className='btn-margin',
        style={'display': 'none'},
    ),
    'lexical_an_btn_rm': dbc.Button(
        "Remover",
        id='lexical-an-btn-rm',
        color='danger',
        outline=True,
        className='btn-margin',
    ),
    'lexical_an_alert': html.Div(
        id='lexical-an-alert',
    ),
    'lexical_an_upload': dcc.Upload(
        id='lexical-an-upload',
        children=html.Div([
            html.A('Upload')
        ]),
        multiple=False,
        className='btn btn-margin btn-outline-dark'
    ),
    'lexical_an_download': html.A(
        "Dowload",
        id='lexical-an-download',
        className='btn btn-margin btn-outline-dark'
    ),
    'lexical_an_pseudo_cod_ta': dbc.Textarea(
        id='lexical-an-pseudo-cod-ta',
        placeholder="Digite o Pseudo Código",
        className='bigarea',
    ),

    'lexical_an_table': DataTable(
        id='lexical-an-table',
        editable=True,
        columns=[
            {'name': 'Lexema', 'id': 'lexema'},
            {'name': 'Token', 'id': 'token'},
        ],
        #filter_action="native",
        #sort_action="native",
        #sort_mode="multi",
        #page_action="native",
        #page_current=0,
        #page_size=10,
    ),

}


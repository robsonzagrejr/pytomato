import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash_table import DataTable


widgets = {
    'sintatic_an_dropdown': dcc.Dropdown(
        id='sintatic-an-dropdown',
    ),
    'sintatic_an_input': dbc.Input(
        id='sintatic-an-input',
        placeholder='Gramatica label',
    ),
    'sintatic_an_text_area': dbc.Textarea(
        id='sintatic-an-text-area',
        placeholder="Digite a Gramática",
        className='bigarea',
    ),
    'sintatic_an_btn_add': dbc.Button(
        "Adicionar",
        id='sintatic-an-btn-add',
        color='dark',
        outline=True,
        className='btn-margin',
    ),
    'sintatic_an_btn_update': dbc.Button(
        "Atualizar",
        id='sintatic-an-btn-update',
        color='secondary',
        outline=True,
        className='btn-margin',
        style={'display': 'none'},
    ),
    'sintatic_an_btn_rm': dbc.Button(
        "Remover",
        id='sintatic-an-btn-rm',
        color='danger',
        outline=True,
        className='btn-margin',
    ),
    'sintatic_an_alert': html.Div(
        id='sintatic-an-alert',
    ),
    'sintatic_an_upload': dcc.Upload(
        id='sintatic-an-upload',
        children=html.Div([
            html.A('Upload')
        ]),
        multiple=False,
       className='btn btn-margin btn-outline-dark'
    ),
    'sintatic_an_download': html.A(
        "Dowload",
        id='sintatic-an-download',
        className='btn btn-margin btn-outline-dark'
    ),
    'sintatic_an_table': DataTable(
        id='sintatic-an-table',
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
    'sintatic_an_items_div': html.Div(
        id='sintatic-an-items-div',
    ),
 
    'sintatic_an_btn_convert_af': dbc.Button(
        "Converter para AF",
        id='sintatic-an-btn-convert-af',
        color='dark',
        outline=True,
        className='btn-margin',
    ),
}


import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash_table import DataTable


widgets = {
    'regular_exp_dropdown': dcc.Dropdown(
        id='regular-exp-dropdown',
    ),
    'regular_exp_input': dbc.Input(
        id='regular-exp-input',
        placeholder='Expressão Regular label',
    ),
    'regular_exp_text_area': dbc.Textarea(
        id='regular-exp-text-area',
        placeholder="Digite a Expressão Regular",
        className='bigarea',
    ),
    'regular_exp_btn_add': dbc.Button(
        "Adicionar",
        id='regular-exp-btn-add',
        color='dark',
        outline=True,
        className='btn-margin',
    ),
    'regular_exp_btn_update': dbc.Button(
        "Atualizar",
        id='regular-exp-btn-update',
        color='secondary',
        outline=True,
        className='btn-margin',
        style={'display': 'none'},
    ),
    'regular_exp_btn_rm': dbc.Button(
        "Remover",
        id='regular-exp-btn-rm',
        color='danger',
        outline=True,
        className='btn-margin',
    ),
    'regular_exp_alert': html.Div(
        id='regular-exp-alert',
    ),
    'regular_exp_upload': dcc.Upload(
        id='regular-exp-upload',
        children=html.Div([
            html.A('Upload')
        ]),
        multiple=False,
        className='btn btn-margin btn-outline-dark'
    ),
    'regular_exp_download': html.A(
        "Dowload",
        id='regular-exp-download',
        className='btn btn-margin btn-outline-dark'
    ),
    'regular_exp_btn_update_from_table': dbc.Button(
        "Atualizar a partir da Tabela",
        id='regular-exp-btn-update-from-table',
        color='secondary',
        outline=True,
        style={'display': 'none'},
    ),
    'regular_exp_table': DataTable(
        id='regular-exp-table',
        editable=True,
        #filter_action="native",
        #sort_action="native",
        #sort_mode="multi",
        #page_action="native",
        #page_current=0,
        #page_size=10,
        style_table={
            'overflow': 'auto',
            'margin': '0 15px 0 15px',
        },
    ),
    'regular_exp_btn_convert_af': dbc.Button(
        "Converter para AF",
        id='regular-exp-btn-convert-af',
        color='dark',
        outline=True,
        className='btn-margin',
    ),
    'regular_exp_helper_alert': html.Div(
        id='regular-exp-helper-alert',
    ),
 
}


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
        placeholder='Automato label',
    ),
    'automaton_text_area': dbc.Textarea(
        id='automaton-text-area',
        placeholder="Digite o Automato",
        className='bigarea',
    ),
    'automaton_btn_add': dbc.Button(
        "Adicionar",
        id='automaton-btn-add',
        color='dark',
        outline=True,
        className='btn-margin',
    ),
    'automaton_btn_update': dbc.Button(
        "Atualizar",
        id='automaton-btn-update',
        color='secondary',
        outline=True,
        className='btn-margin',
        style={'display': 'none'},
    ),
    'automaton_btn_rm': dbc.Button(
        "Remover",
        id='automaton-btn-rm',
        color='danger',
        outline=True,
        className='btn-margin',
    ),
    'automaton_alert': html.Div(
        id='automaton-alert',
    ),
    'automaton_upload': dcc.Upload(
        id='automaton-upload',
        children=html.Div([
            html.A('Upload')
        ]),
        multiple=False,
        className='btn btn-margin btn-outline-dark'
    ),
    'automaton_download': html.A(
        "Dowload",
        id='automaton-download',
        className='btn btn-margin btn-outline-dark'
    ),

    #Table
    'automaton_btn_update_from_table': dbc.Button(
        "Atualizar a partir da Tabela",
        id='automaton-btn-update-from-table',
        color='secondary',
        outline=True,
        style={'display': 'none'},
    ),
    'automaton_table': DataTable(
        id='automaton-table',
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
    'automaton_btn_collapse_tip': dbc.Button(
        "?",
        id='automaton-btn-collapse-tip',
        color='dark',
        outline=True,
        size='sm'

    ),
    'automaton_operation_dropdown': dcc.Dropdown(
        id='automaton-operation-dropdown',
        options = [
            {'label': 'Minimização', 'value': 'minimization'},
            {'label': 'Determinização', 'value': 'determinization'},
            {'label': 'União', 'value': 'union'},
            {'label': 'Intercessão', 'value': 'intersection'},
        ],
        multi=False,
        value='minimization'
    ),
    'automaton_second_dropdown': dcc.Dropdown(
        id='automaton-second-dropdown',
    ),
    'automaton_btn_apply_operation': dbc.Button(
        "Aplicar Operação",
        id='automaton-btn-apply-operation',
        color='dark',
        outline=True,
        className='btn-margin',
    ),
    'automaton_btn_convert_gr': dbc.Button(
        "Converter para GR",
        id='automaton-btn-convert-gr',
        color='dark',
        outline=True,
        className='btn-margin',
    ),
    'automaton_btn_modal_execution': dbc.Button(
        "Verificar palavra",
        id='automaton-btn-modal-execution',
        color='dark',
        outline=True,
        className='btn-margin',
    ),
    'automaton_modal_execution': dbc.Modal(
        [
            dbc.ModalHeader("Verificar se AF aceita palavra"),
            dbc.ModalBody(
                [
                    dbc.Input(id='automaton-check-word-input', placeholder='Palavra'),
                    html.Br(),
                    dbc.Button("Verificar", id="automaton-btn-check-word", className="ml-auto"),
                ]
            ),
            dbc.ModalFooter(
                [
                    html.Div(id="automaton-check-word-alert", className='ml-auto'),
                ]
            ),
        ],
        id="automaton-check-word-modal",
    ),

    'automaton_graph': html.Div(
        [
            html.Div(id='automaton-graph', className='graphvis'),
            html.Div(id='automaton-graph-help'),
        ]
    )
}


import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash_table import DataTable


widgets = {
    'grammar_text_area': dbc.Textarea(
        id='grammar-text-area',
        placeholder="Digite a Gramática"
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


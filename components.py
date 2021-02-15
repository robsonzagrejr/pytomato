import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash_table import DataTable


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Gramática", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("v", header=True),
                dbc.DropdownMenuItem("Automato", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="Linguagens Formais",
    brand_href="#",
    color="dark",
    dark=True,
)

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
    'automaton_table': DataTable(
        id='automaton-table',
        columns=[
            {'name': ' ', 'id':' '},
            {'name': 'num', 'id':'num'},
            {'name': 'id', 'id': 'id'},
            {'name': 'assign', 'id':'assign'},
            {'name': 'S', 'id':'S'},
            {'name': 'E', 'id':'E'},
            {'name': 'V', 'id':'V'},
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
    )
}


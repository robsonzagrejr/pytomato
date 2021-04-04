"""Importações

Importação das biblioteca dash de componetes necessárias.
"""
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash_table import DataTable

"""Config. Barra de Navegação

Define a configuração da barra de navegação para cada página.
"""
def make_navbar(url_base):
    return dbc.NavbarSimple(
        id='navbar',
        children=[
            dbc.NavItem(dbc.NavLink("Gramática", href=f"{url_base}grammar")),
            dbc.NavItem(dbc.NavLink("Automato", href=f"{url_base}automaton")),
            dbc.NavItem(dbc.NavLink("Expressão Regular", href=f"{url_base}regular_exp")),
        ],
        brand="Pytomato",
        brand_href="#",
        color="dark",
        dark=True,
    )

stores = {
    'store-grammar': dcc.Store(data={}, id='store-grammar', storage_type='local'),
    'store-automaton': dcc.Store(data={}, id='store-automaton', storage_type='local'),
    'store-regular-exp': dcc.Store(data={}, id='store-regular-exp', storage_type='local'),
}

page_content = html.Div(
    [
        dcc.Location(id='url', refresh=False),
        stores['store-grammar'],
        stores['store-automaton'],
        stores['store-regular-exp'],
        html.Div(id='page-content'),
    ]
)




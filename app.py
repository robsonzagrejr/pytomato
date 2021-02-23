""" Importe Dependências 

Importação da framework Dash e das blibliotecas para
utilizar componetes Bootstrap e HTML.
"""
from dash import Dash
import dash_bootstrap_components as dbc
import dash_html_components as html

from core.components import (
    make_navbar,
    page_content
)

from core.callbacks import register_callbacks

"""Instância Dash

Dash instanciado, definindo framework Bootstrap como base
para criação dos componentes.
"""
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True

#Definição do Título
app.title = 'Linguagens Formais'


url_base = '/'
if app.config['url_base_pathname'] is not None:
    url_base = app.config['url_base_pathname']

"""Definição Layout

Define e retorna o conteúdo HTML que será apresentado
na página web.
"""
def serve_layout():
    return html.Div(
        children=[
            make_navbar(url_base),
            page_content
        ]
    )
# Atribui o layout 
app.layout=serve_layout()
# Registra os callbacks
register_callbacks(app)

# Inicia o servidor no IP 0.0.0.0/8080
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True)


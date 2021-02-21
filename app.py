from dash import Dash
import dash_bootstrap_components as dbc
import dash_html_components as html

from core.components import (
    make_navbar,
    page_content
)

from core.callbacks import register_callbacks


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True

app.title = 'Linguagens Formais'


url_base = '/'
if app.config['url_base_pathname'] is not None:
    url_base = app.config['url_base_pathname']

app.layout = html.Div(
    children=[
        make_navbar(url_base),
        page_content
    ]
)

register_callbacks(app)


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True)


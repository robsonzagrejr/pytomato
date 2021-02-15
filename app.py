from dash import Dash
import dash_bootstrap_components as dbc
import dash_html_components as html

from layout import (
    header,
    inputs,
    outputs
)
from components import navbar
from callbacks import register_callbacks


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True

app.title = 'Linguagens Formais'

app.layout = html.Div(
    children=[
        navbar,
        header,
        inputs,
        outputs
    ]
)

register_callbacks(app)


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True)


import dash
from dash import html, dcc


dash.register_page(
    __name__,
    title = 'Dados do Modelo',
    name  = 'Dados do Modelo'
)

layout = html.Div(children=[
   
    html.H1(children='Under Construction'),

    html.H2(children='Don''t you worry. You still have 3 more pages to enjoy')

],className="bodyContent")
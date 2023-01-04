import dash
from dash import html, dcc

dash.register_page(__name__)

dash.register_page(
    __name__,
    path ='/',
    title = 'Home',
    name  = 'Home'
)


layout = html.Div(children=[
    
    #------------------------------------------------------------------------------------------
    #Grafico de Tensao
    html.Div([

        html.H1(children='Bem-Vindo!'),
        html.P(children='Esse website foi elaborado para automatizar a geração de gráficos e análises dos resultados obtidos por meio de algoritmos de Fluxo de Potência'),
        html.P(children='Sua estrutura foi desenvolvida em Python Dash e hospedada utilizando-se OnRender. Para a programação utilizou-se as bibliotecas Python Pandas e Plotly, combinadas com as linguagens de programação web HTML e CSS'),
        

    ],className="textoCorpo"), 

],className="bodyContent")
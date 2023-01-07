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
        html.P(children='Seu intuito é proporcionar uma maior eficiência nesse processo, que por vezes e, especialmente em modelos maiores, demanda um tempo considerável do dia a dia do pesquisador'),
        html.P(children='Sua estrutura foi desenvolvida em Python Dash e hospedada utilizando-se OnRender. Para a programação utilizou-se as bibliotecas Python Pandas e Plotly, combinadas com as linguagens de programação web HTML e CSS'),
        html.Div([
            html.Img(src="../assets/imagens/python.png",className="techIcon"),
            html.Img(src="../assets/imagens/python_dash.png",className="techIcon"),
            html.Img(src="../assets/imagens/pandas.png",className="techIcon"),
            html.Img(src="../assets/imagens/html.png",className="techIcon"),
            html.Img(src="../assets/imagens/css.png",className="techIcon"),
        ],className="tecnologiasUtilizadas"),
        html.P(children='Esse trabalho é mais um dos resultados advindos do projeto de pesquisa "Estudo, implementação e validação de métodos de controle em redes elétricas na presença de geração distribuída intermitente", e fruto de uma parceria entre o Laboratório de Pesquisa e Inovação em Sistemas Elétricos de Potência (LAPI-SEP) da UFMT, com o Laboratório de Análise Computacional em Sistemas Elétricos de Potência (LacoSEP), da EESC-USP'),
        html.Div([
            html.Img(src="../assets/imagens/logoUFMT.png",className="institutionIcon"),
            html.Img(src="../assets/imagens/EESC_USP.png",className="institutionIcon"),
        ],className="tecnologiasUtilizadas"),
        html.P(children='Esse site é continuamente atualizado e novas funcionalidades vem sendo acrescentadas desde sua origem. Por favor, caso hajam sugestões, favor informar para o e-mail: cristhiangro@gmail.com'),
        html.P(children='Um ótimo trabalho a todos!'),
        html.P(children='OLIVEIRA, C. G. R., JAN, 2023')
        

    ],className="textoCorpo"), 

],className="bodyContent")
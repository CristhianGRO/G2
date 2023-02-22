from dash import Dash, html, dcc
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import dash


dash.register_page(
    __name__,
    title = 'Dados de Controle',
    name  = 'Dados de Controle'
)

#===========================================================================================
#Function that read the input data_CapacitorBank file
#===========================================================================================
barraCapacitorBank = []
capacitoresTotais = []

def readInputCapacitorBank():
    dataFile = open("data_CapacitorBank_Dynamic.txt","r")
    linhas = dataFile.readlines()
    j=0
    for linha in linhas:
        if j != 0:
            Barra = int(linha.split(" ",2)[0])
            barraCapacitorBank.append(Barra)
            capTotal = int(linha.split(" ",5)[3])
            capacitoresTotais.append(capTotal)
        else:
            nCapacitorBank=int(linha.split(" ",2)[0])
        j=j+1
    return nCapacitorBank

nCapacitorBank = readInputCapacitorBank()

hora=[]
ihora = 1

for j in range(24):
    hora.append(ihora)
    ihora = ihora+1

#===========================================================================================
#Function that read the input HISTORIC_BC file
#===========================================================================================
capacitoresChaveadosTemporary = []
capacitoresChaveados = []

def readHistoricCapacitorBank():
    dataFile = open("HISTORIC_CB.txt","r")
    linhas = dataFile.readlines()
    j=0
    for linha in linhas:
        capacitoresChaveadosTemporary.append([])
        for k in range(nCapacitorBank):
            nChaveado = int(linha.split(" ",nCapacitorBank)[k])
            capacitoresChaveadosTemporary[j].append(nChaveado)    
        j=j+1

readHistoricCapacitorBank()

for i in range(nCapacitorBank):
    capacitoresChaveados.append([])
    for j in range(24):
        capacitoresChaveados[i].append(capacitoresChaveadosTemporary[j][i])
       

#===========================================================================================
#Making the hour generation Figure
#===========================================================================================
k=0
fig_CapacitorBank = go.Figure(data=[go.Scatter(name="Barra BC: {}".format(barraCapacitorBank[0]),x=hora, y=capacitoresChaveados[0])])
for i in range(1,nCapacitorBank):
    fig_CapacitorBank.add_trace(go.Scatter(name = "Barra BC: {}".format(barraCapacitorBank[i]),x=hora, y=capacitoresChaveados[i]))
fig_CapacitorBank.update_layout(legend_valign="middle")


#===========================================================================================
#Making some Analysis
#===========================================================================================
somaChaveado = []

for i in range(24):
    soma = 0
    for j in range(nCapacitorBank):
        soma += capacitoresChaveados[j][i]
    somaChaveado.append(soma)
maximoChaveado = max(somaChaveado)

margemControle = (1-maximoChaveado/sum(capacitoresTotais))*100

horaCritica = somaChaveado.index(maximoChaveado) + 1

maxBC = max(capacitoresChaveados)
barraMaxBC = capacitoresChaveados.index(maxBC)
BCmaisCritico = barraCapacitorBank[barraMaxBC]

#===========================================================================================
#Layout de exibicao HTML
#===========================================================================================
layout = html.Div(children=[
    
 
    html.Div([
        html.H1(children='Dados de Controle',className='titulo_secao'),
    ],className='div_titulo_secao'),

    
       
       html.Div([
          html.P('Número de Capacitores Chaveados por Banco'),
     
            dcc.Graph(
                id='grafico_loadCurve',
                figure=fig_CapacitorBank
            )
        ],id="wideGraph_green"),


        html.Div([
            html.Div([
                html.P('BC mais Crítico'),
                html.H1(children="{}".format(BCmaisCritico),id="id_nBus",style={'margin-left':'2.5em'}),
            ],id="halfGraph_red"),

            html.Div([
                html.P('Margem de Controle'),
                html.H1(children="{:.2f}%".format(margemControle),id="id_nBranch",style={'margin-left':'1.2em'}),
            ],id="halfGraph_blue"), 

            html.Div([
                html.P('Hora mais Crítica'),
                html.H1(children="{:02d}:00h".format(horaCritica),id="id_nBranch",style={'margin-left':'1.2em'}),
            ],id="halfGraph_yellow"), 
        ],className="halfDivConfig"),
       

   
],className="bodyContent")
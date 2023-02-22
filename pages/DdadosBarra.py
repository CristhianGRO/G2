from dash import Dash, html, dcc
import pandas as pd
import plotly.graph_objs as go
import math
import dash

dash.register_page(__name__)

dash.register_page(
    __name__,
    title = 'Dados de Barra',
    name  = 'Dados de Barra'
)

dataBus = []
id = []
#===========================================================================================
#Function that read the input data_bus file
#===========================================================================================
def readInputBus():
    dataFile = open("data_Bus.txt","r")
    linhas = dataFile.readlines()
    j=0
    for linha in linhas:
        if j != 0:
            idJ=linha.split(",",2)[0] 
            id.append(idJ)
            type=linha.split(",",2)[1]
            dataBus.append([])
            dataBus[j-1].append(id)
            dataBus[j-1].append(type)
            Pd=linha.split(",",5)[2]
            Qd=linha.split(",",5)[3]
            dataBus[j-1].append(Pd)
            dataBus[j-1].append(Qd)
        else:
            nBus=int(linha.split(",",2)[0])
        j=j+1
    return nBus

nBus    = readInputBus()
tensao = []
moduloTensao   = []
anguloTensao   = []
results = []

#===========================================================================================
#Function that read the input results file
#===========================================================================================
def importResults():
    dataFile = open("results.txt","r")
    linhas = dataFile.readlines()
   
    for linha in linhas:
        for i in range(0,2*nBus,2):
            modulo = float(linha.split(" ",2*nBus)[i])
            angulo = float(linha.split(" ",2*nBus)[i+1])
            moduloTensao.append(modulo)
            anguloTensao.append(angulo*180/math.pi)
        

importResults()

tensaoControle       = []
moduloTensaoControle = []
anguloTensaoControle = []
resultsControle = []

#===========================================================================================
#Function that read the input results_controle file
#===========================================================================================
def importResultsControle():
    dataFile = open("results_controle.txt","r")
    linhas = dataFile.readlines()
   
    for linha in linhas:
        for i in range(0,2*nBus,2):
            moduloControle = float(linha.split(" ",2*nBus)[i])
            anguloControle = float(linha.split(" ",2*nBus)[i+1])
            moduloTensaoControle.append(moduloControle)
            anguloTensaoControle.append(anguloControle*180/math.pi)

importResultsControle()


id = id*24
hora=[]
ihora = 1

for j in range(24):
    hora.append(ihora)
    ihora = ihora+1

df = pd.DataFrame({
    "Id": id,
    "Tensao": moduloTensao,
    "Angulo": anguloTensao,
    "TensaoControle": moduloTensaoControle,
    "AnguloControle": anguloTensaoControle,
})

#===========================================================================================
#Making the voltage Vector used to construct the voltage figure
#===========================================================================================
tensoes = []
tensoesControle = []
for i in range(1,nBus+1,1):
    newdf = df.query('Id == "{}"'.format(i))
    tensaoAtual = newdf["Tensao"].tolist()
    tensoes.append(tensaoAtual)
    tensaoAtualControle = newdf["TensaoControle"].tolist()
    tensoesControle.append(tensaoAtualControle)

#===========================================================================================
#Making the angle Vector used to construct the angle figure
#===========================================================================================
angulos = []
angulosControle = []
for i in range(1,nBus+1,1):
    newdf = df.query('Id == "{}"'.format(i))
    angAtual = newdf["Angulo"].tolist()
    angulos.append(angAtual)
    angAtualControle = newdf["AnguloControle"].tolist()
    angulosControle.append(angAtualControle)

#===========================================================================================
#Making some Analysis
#===========================================================================================
#Voltage Analysis
maxTensaoHoraria = []
maxTensaoHorariaControle = []

for i in tensoes:
    maxTensaoHoraria.append(max(i))
maxTensao = max(maxTensaoHoraria)
barraMaxTensao = maxTensaoHoraria.index(maxTensao) + 1

for i in tensoesControle:
    maxTensaoHorariaControle.append(max(i))
maxTensaoControle = max(maxTensaoHorariaControle)
barraMaxTensaoControle = maxTensaoHorariaControle.index(maxTensaoControle) + 1

minTensaoHoraria = []
minTensaoHorariaControle = []

for i in tensoes:
    minTensaoHoraria.append(min(i))
minTensao = min(minTensaoHoraria)
barraMinTensao = minTensaoHoraria.index(minTensao) + 1

for i in tensoesControle:
    minTensaoHorariaControle.append(min(i))
minTensaoControle = min(minTensaoHorariaControle)
barraMinTensaoControle = minTensaoHorariaControle.index(minTensaoControle) + 1

#===========================================================================================
#Making the voltage Figure
#===========================================================================================

fig_tensao = go.Figure(data=[go.Scatter(name="Barra {}".format(1),x=hora, y=tensoes[0])])
for i in range(1,nBus):
    fig_tensao.add_trace(go.Scatter(name = "Barra {}".format(i+1),x=hora, y=tensoes[i]))

fig_tensao.update_layout(legend_valign="middle")

fig_tensaoControle = go.Figure(data=[go.Scatter(name="Barra {}".format(1),x=hora, y=tensoesControle[0])])
for i in range(1,nBus):
    fig_tensaoControle.add_trace(go.Scatter(name = "Barra {}".format(i+1),x=hora, y=tensoesControle[i]))

fig_tensaoControle.update_layout(legend_valign="middle")
#===========================================================================================
#Making the angle Figure
#===========================================================================================
fig_angulo = go.Figure(data=[go.Scatter(name="Barra {}".format(1),x=hora, y=angulos[0])])
for i in range(1,nBus):
    fig_angulo.add_trace(go.Scatter(name = "Barra {}".format(i+1),x=hora, y=angulos[i]))

fig_angulo.update_layout(legend_valign="middle")

fig_anguloControle = go.Figure(data=[go.Scatter(name="Barra {}".format(1),x=hora, y=angulosControle[0])])
for i in range(1,nBus):
    fig_anguloControle.add_trace(go.Scatter(name = "Barra {}".format(i+1),x=hora, y=angulosControle[i]))

fig_anguloControle.update_layout(legend_valign="middle")



layout = html.Div(children=[
    
    #======================================================================
    #DADOS ANTES DA IMPLEMENTAÇÃO DO CONTROLE
    #======================================================================

    #Grafico de Tensao
        html.Div([
            html.H1(children='Dados de Barra - Sem Controle',className='titulo_secao'),
        ],className='div_titulo_secao'),

         html.Div([
        html.Div([
            html.P('Módulo de Tensão Horário [p.u.]'),
            
            dcc.Graph(
                id='grafico_tensao',
                figure=fig_tensao
            )
        ],id="wideGraph_green"),
    #------------------------------------------------------------------------------------------
    #Analise de Tensao
    html.Div([

        html.Div([
            html.P('Máxima Tensão'),
            html.H1(children="{:.3f} [p.u.]".format(maxTensao),id="id_maxTensao"),
         ],id="halfGraph_green"),


          html.Div([
            html.P('Mínima Tensão'),
            html.H1(children="{:.3f} [p.u.]".format(minTensao),id="id_minTensao"),
            ],id="halfGraph_red"), 

        html.Div([
            html.P('Barras Críticas'),
            html.H2(children="Máx.: {}".format(barraMaxTensao),id="id_horaPicoInf"),
            html.H2(children="Mín. : {}".format(barraMinTensao),id="id_horaPicoSup"),
            ],id="halfGraph_blue"), 
    ],className="halfDivConfig"),
    ]),
    #------------------------------------------------------------------------------------------
    #Grafico de Angulo de fase
    html.Div([
        html.Div([
            html.P('Ângulo de Fase Horário [deg]'),
            
            dcc.Graph(
                id='grafico_angulo',
                figure=fig_angulo
            )
        ],id="wideGraph_blue"),
    ]),

    #======================================================================
    #DADOS APÓS A IMPLEMENTAÇÃO DO CONTROLE
    #======================================================================

    #Grafico de Tensao
        html.Div([
            html.H1(children='Dados de Barra - Controle Local Clássico',className='titulo_secao'),
        ],className='div_titulo_secao'),

         html.Div([
        html.Div([
            html.P('Módulo de Tensão Horário [p.u.]'),
            
            dcc.Graph(
                id='grafico_tensao',
                figure=fig_tensaoControle
            )
        ],id="wideGraph_green"),
    #------------------------------------------------------------------------------------------
    #Analise de Tensao
    html.Div([

        html.Div([
            html.P('Máxima Tensão'),
            html.H1(children="{:.3f} [p.u.]".format(maxTensaoControle),id="id_maxTensao"),
         ],id="halfGraph_green"),


          html.Div([
            html.P('Mínima Tensão'),
            html.H1(children="{:.3f} [p.u.]".format(minTensaoControle),id="id_minTensao"),
            ],id="halfGraph_red"), 

        html.Div([
            html.P('Barras Críticas'),
            html.H2(children="Máx.: {}".format(barraMaxTensaoControle),id="id_horaPicoInf"),
            html.H2(children="Mín. : {}".format(barraMinTensaoControle),id="id_horaPicoSup"),
            ],id="halfGraph_blue"), 
    ],className="halfDivConfig"),
    ]),
    #------------------------------------------------------------------------------------------
    #Grafico de Angulo de fase
    html.Div([
        html.Div([
            html.P('Ângulo de Fase Horário [deg]'),
            
            dcc.Graph(
                id='grafico_angulo',
                figure=fig_anguloControle
            )
        ],id="wideGraph_blue"),
    ]),

],className="bodyContent")
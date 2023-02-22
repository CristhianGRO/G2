from dash import Dash, html, dcc
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import dash


dash.register_page(
    __name__,
    title = 'Dados do Modelo',
    name  = 'Dados do Modelo'
)






#===========================================================================================
#Function that read the input data_bus file
#===========================================================================================
dataBus = []
idBus = []
def readInputBus():
    dataFile = open("data_Bus.txt","r")
    linhas = dataFile.readlines()
    j=0
    for linha in linhas:
        if j != 0:
            idJ=linha.split(",",2)[0] 
            idBus.append(idJ)
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

#===========================================================================================
#Function that read the input data_branch file
#===========================================================================================
dataBranch = []
def readInputBranch():
    dataFile = open("data_Branch.txt","r")
    linhas = dataFile.readlines()
    j=0
    for linha in linhas:
        if j != 0:
            fBus=linha.split(",",2)[0]
            tBus=linha.split(",",2)[1]
            dataBranch.append([])
            dataBranch[j-1].append(fBus)
            dataBranch[j-1].append(tBus)
        else:
            nBranch=int(linha.split(",",2)[0])
        j=j+1
    return nBranch

nBranch = readInputBranch()
#===========================================================================================
#Function that read the input data_Photovoltaic file
#===========================================================================================
barraPhotovoltaic = []
dadosGeracao = []
Ppico = []

def readInputPhotovoltaic():
    dataFile = open("data_Photovoltaic.txt","r")
    linhas = dataFile.readlines()
    j=0
    for linha in linhas:
        if j != 0:
            Barra = int(linha.split(" ",2)[0])
            Ppicoj = float(linha.split(" ",2)[1])
            barraPhotovoltaic.append([])
            Ppico.append([])
            dadosGeracao.append([])
            for i in range(24):
                barraPhotovoltaic[j-1].append(Barra)
                Ppico[j-1].append(Ppicoj)
                geradoHora = float(linha.split(" ",27)[i+2])
                dadosGeracao[j-1].append(geradoHora)
        else:
            nPhotovoltaic=int(linha.split(" ",2)[0])
        j=j+1
    return nPhotovoltaic

nPhotovoltaic = readInputPhotovoltaic()

dadosLoadCurve = []
barraLoadCurve = []
#===========================================================================================
#Function that read the input data_LoadCurve file
#===========================================================================================
def readInputLoadCurve():
    dataFile = open("data_LoadCurve.txt","r")
    linhas = dataFile.readlines()
    j=0
    for linha in linhas:
        if j != 0:
            Barra = linha.split(" ",2)[0]
            barraLoadCurve.append([])
            dadosLoadCurve.append([])
            for i in range(24):
                barraLoadCurve[j-1].append(Barra)
                loadCurveHora = float(linha.split(" ",27)[i+1])
                dadosLoadCurve[j-1].append(loadCurveHora)  
        else:
            nLoadCurve=int(linha.split(" ",2)[0])
        j=j+1
    return nLoadCurve

nLoadCurve = readInputLoadCurve()

horaFV = []
hora=[]
horaLC = []
ihora = 1

for j in range(24):
    hora.append(ihora)
    ihora = ihora+1


if nPhotovoltaic > 1:
    for j in range(nPhotovoltaic):
        horaFV.append(hora)
else:
    horaFV = hora

if nLoadCurve > 1:
    for j in range(nLoadCurve):
        horaLC.append(hora)


dfPhotovoltaic = pd.DataFrame({
    "Barra": barraPhotovoltaic,
    "Hora":  horaFV,
    "Geracao_Horaria": dadosGeracao,
    "Potencia_Pico": Ppico
})

dfLoadCurve = pd.DataFrame({
    "Barra": barraLoadCurve,
    "Hora":  horaLC,
    "Curva_de_Carga": dadosLoadCurve,
})
#===========================================================================================
#Making the hour generation Vector used to construct the generation figure
#===========================================================================================
geracaoHoraria = []
k=0
for i in range(nPhotovoltaic):
    geracaoHoraria.append([])
    for j in range(24):
        geracaoHorariaAtual = dadosGeracao[i][j] * Ppico[i][j]
        geracaoHoraria[k].append(geracaoHorariaAtual)
    k += 1
   
#===========================================================================================
#Making the hour load curve Vector used to construct the load curve figure
#===========================================================================================
curvaDeCargaHoraria = []
k=0
for i in range(nLoadCurve):
    curvaDeCargaHoraria.append([])
    for j in range(24):
        curvaDeCargaAtual = dadosLoadCurve[i][j]
        curvaDeCargaHoraria[k].append(curvaDeCargaAtual)
    k += 1


#===========================================================================================
#Making the hour generation Figure
#===========================================================================================
fig_geracaoSolar = go.Figure(data=[go.Scatter(name="Barra de Geração: {}".format(barraPhotovoltaic[0][0]),x=horaFV, y=geracaoHoraria[0])])
for i in range(1,nPhotovoltaic):
    fig_geracaoSolar.add_trace(go.Scatter(name = "Barra de Geração: {}".format(barraPhotovoltaic[i][0]),x=horaFV, y=geracaoHoraria[i]))

fig_geracaoSolar.update_layout(legend_valign="middle")



#===========================================================================================
#Making the hour load Curve Figure
#===========================================================================================
fig_loadCurve = go.Figure(data=[go.Scatter(name="Barra de Carga: {}".format(barraLoadCurve[0][0]),x=horaLC, y=curvaDeCargaHoraria[0])])
for i in range(1,nLoadCurve):
    fig_loadCurve.add_trace(go.Scatter(name = "Barra de Carga: {}".format(barraLoadCurve[i][0]),x=horaLC, y=curvaDeCargaHoraria[i]))

fig_loadCurve.update_layout(legend_valign="middle")



#===========================================================================================
#Making some Analysis
#===========================================================================================
#Getting the total Load of the model
totalMW = 0
totalMVar = 0

for i in range(nBus):
    totalMW   += float(dataBus[i][2])
    totalMVar += float(dataBus[i][3]) 

#Get the total peak installed generation in the system
geracaoTotalPico = 0
for i in range(nPhotovoltaic):
    geracaoTotalPico += Ppico[i][0]

#Get the host percentual of the system
hospedagem = geracaoTotalPico/totalMW *100

#Get the higher generation bus of the system (considering the energy along the day)
PV_energy = []
for i in range(nPhotovoltaic):
    PV_energy.append(sum(geracaoHoraria[i]))

maximaGeracao = max(PV_energy)
barraMaiorGeracao_index = PV_energy.index(maximaGeracao)
barraMaiorGeracao = barraPhotovoltaic[barraMaiorGeracao_index][0]

#===========================================================================================
#Layout de exibicao HTML
#===========================================================================================
layout = html.Div(children=[
    
 
    html.Div([
        html.H1(children='Dados do Modelo',className='titulo_secao'),
    ],className='div_titulo_secao'),

    html.Div([
        html.P('Diagrama Unifilar'),
     
        html.Img(src="../assets/imagens/modelo_70_barras.jpg",style={'width': '100%'}),
    ],id="wideGraph_yellow"),
    
    

        #------------------------------------------------------------------------------------------
        #Analise de Modelo
        html.Div([
            html.Div([
                html.P('Número de Barras'),
                html.H1(children="{}".format(nBus),id="id_nBus",style={'margin-left':'2.5em'}),
            ],id="halfGraph_green"),

            html.Div([
                html.P('Número de Linhas'),
                html.H1(children="{}".format(nBranch),id="id_nBranch",style={'margin-left':'2.5em'}),
            ],id="halfGraph_yellow"), 

            html.Div([
                html.P('Carga total:'),
                html.H2(children="{:.3f} [p.u.]".format(totalMW),id="id_totalMW"),
                html.H2(children="{:.3f} [p.u.]".format(totalMVar),id="id_totalMVar"),
            ],id="halfGraph_red"), 
        ],className="halfDivConfig"),
       
       html.Div([
          html.P('Curva de Carga Horária'),
     
            dcc.Graph(
                id='grafico_loadCurve',
                figure=fig_loadCurve
            )
        ],id="wideGraph_green"),

        html.Div([
          html.P('Geração Solar Horária'),
     
            dcc.Graph(
                id='grafico_geracaoSolar',
                figure=fig_geracaoSolar
            )
        ],id="wideGraph_blue"),

        html.Div([
            html.Div([
                html.P('Geração de Pico Instalada'),
                html.H1(children="{:.3f} p.u.".format(geracaoTotalPico),id="id_nBus",style={'margin-left':'0.2em'}),
            ],id="halfGraph_green"),

            html.Div([
                html.P('Hospedagem'),
                html.H1(children="{:.2f}%".format(hospedagem),id="id_nBranch",style={'margin-left':'1.2em'}),
            ],id="halfGraph_blue"), 

            html.Div([
                html.P('Barra de maior geração'),
                html.H2(children="{}".format(barraMaiorGeracao),id="id_totalMW",style={'margin-left':'3.5em'}),
                html.H2(children="{:.3f} p.u.".format(maximaGeracao),id="id_totalMVar",style={'margin-left':'1.8em'}),
            ],id="halfGraph_yellow"), 
        ],className="halfDivConfig"),
       

   
],className="bodyContent")
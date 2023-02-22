from dash import Dash, html, dcc
import pandas as pd
import plotly.graph_objs as go
import math
import dash

dash.register_page(__name__)

dash.register_page(
    __name__,
    title = 'Dados de Trecho',
    name  = 'Dados de Trecho'
)

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

#===========================================================================================
dataBus = []
id = []
#===========================================================================================
#Function that read the input data_branch file
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
        else:
            nBus=int(linha.split(",",2)[0])
        j=j+1
    return nBus

nBus    = readInputBus()
nBranch = readInputBranch()
tensao = []
moduloTensao   = []
anguloTensao   = []
perdasAtivas   = []
perdasReativas = []
results = []

moduloTensaoControle   = []
anguloTensaoControle   = []
perdasAtivasControle   = []
perdasReativasControle = []
resultsControle = []

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
    for linha in linhas:
        for i in range(2*nBus,2*nBus+2*nBranch,2):
            perdaAtiva = float(linha.split(" ",2*(nBus+nBranch)+2)[i])
            perdaReativa = float(linha.split(" ",2*(nBus+nBranch)+2)[i+1])
            perdasAtivas.append(perdaAtiva)
            perdasReativas.append(perdaReativa)
        

importResults()

#===========================================================================================
#Function that read the input results_controle file
#===========================================================================================
def importResultsControle():
    dataFile = open("results_controle.txt","r")
    linhas = dataFile.readlines()
   
    for linha in linhas:
        for i in range(0,2*nBus,2):
            modulo = float(linha.split(" ",2*nBus)[i])
            angulo = float(linha.split(" ",2*nBus)[i+1])
            moduloTensaoControle.append(modulo)
            anguloTensaoControle.append(angulo*180/math.pi)
    for linha in linhas:
        for i in range(2*nBus,2*nBus+2*nBranch,2):
            perdaAtiva = float(linha.split(" ",2*(nBus+nBranch)+2)[i])
            perdaReativa = float(linha.split(" ",2*(nBus+nBranch)+2)[i+1])
            perdasAtivasControle.append(perdaAtiva)
            perdasReativasControle.append(perdaReativa)
        

importResultsControle()

hora=[]
ihora = 1

for j in range(24):
    hora.append(ihora)
    ihora = ihora+1


idBranch = []
for i in range(1,nBranch+1,1):
    idBranch.append("{}".format(i))
idBranch = idBranch*24


dfBranch = pd.DataFrame({
    "Id": idBranch,
    "Perdas_Ativas": perdasAtivas,
    "Perdas_Reativas": perdasReativas,
    "Perdas_AtivasControle": perdasAtivasControle,
    "Perdas_ReativasControle": perdasReativasControle,
})
   

#===========================================================================================
#Making the active loses Vector used to construct the loses figure
#===========================================================================================
perdasP = []
perdasQ = []
for i in range(1,nBranch+1,1):
    newdfBranch = dfBranch.query('Id == "{}"'.format(i))
    perdaPAtual = newdfBranch["Perdas_Ativas"].tolist()
    perdasP.append(perdaPAtual)

for i in range(1,nBranch+1,1):
    newdfBranch = dfBranch.query('Id == "{}"'.format(i))
    perdaQAtual = newdfBranch["Perdas_Reativas"].tolist()
    perdasQ.append(perdaQAtual)

perdasPControle = []
perdasQControle = []
for i in range(1,nBranch+1,1):
    newdfBranchControle = dfBranch.query('Id == "{}"'.format(i))
    perdaPAtual = newdfBranchControle["Perdas_AtivasControle"].tolist()
    perdasPControle.append(perdaPAtual)

for i in range(1,nBranch+1,1):
    newdfBranchControle = dfBranch.query('Id == "{}"'.format(i))
    perdaQAtual = newdfBranchControle["Perdas_ReativasControle"].tolist()
    perdasQControle.append(perdaQAtual)
#===========================================================================================
#Making some Analysis
#===========================================================================================
#Losses Analysis
maxPerdaPHoraria = max(perdasP)
maxPerdaP = max(maxPerdaPHoraria)
perdasPTotal = 0

maxPerdaPHorariaControle = max(perdasPControle)
maxPerdaPControle = max(maxPerdaPHorariaControle)
perdasPTotalControle = 0

#Searching for the maximal total loss
perdasP_maxTotal = 0
perdasPControle_maxTotal = 0
for i in range(24):
    somaPerdaPHora = 0
    somaPerdaPHoraControle = 0
    for j in range(nBranch):
        somaPerdaPHora += perdasP[j][i]
        perdasPTotal += perdasP[j][i]
        somaPerdaPHoraControle += perdasPControle[j][i]
        perdasPTotalControle += perdasPControle[j][i]
    if(somaPerdaPHora>perdasP_maxTotal):
        perdasP_maxTotal = somaPerdaPHora
    if(somaPerdaPHoraControle>perdasPControle_maxTotal):
        perdasPControle_maxTotal = somaPerdaPHoraControle
    

reducaoPerdasP = (1-perdasPTotalControle/perdasPTotal)*100

minPerdaPHoraria = min(perdasP)
minPerdaP = min(minPerdaPHoraria)

minPerdaPHorariaControle = min(perdasPControle)
minPerdaPControle = min(minPerdaPHorariaControle)

#===========================================================================================
#Making the active Loss Figure
#===========================================================================================
fig_perdasAtivas = go.Figure(data=[go.Scatter(name="Ramo {}".format(1),x=hora, y=perdasP[0])])
for i in range(1,nBranch):
    fig_perdasAtivas.add_trace(go.Scatter(name = "Ramo {}".format(i+1),x=hora, y=perdasP[i]))

fig_perdasAtivas.update_layout(legend_valign="middle")


fig_perdasAtivasControle = go.Figure(data=[go.Scatter(name="Ramo {}".format(1),x=hora, y=perdasPControle[0])])
for i in range(1,nBranch):
    fig_perdasAtivasControle.add_trace(go.Scatter(name = "Ramo {}".format(i+1),x=hora, y=perdasPControle[i]))

fig_perdasAtivasControle.update_layout(legend_valign="middle")

#===========================================================================================
#Making the reactive Loss Figure
#===========================================================================================
fig_perdasReativas = go.Figure(data=[go.Scatter(name="Ramo {}".format(1),x=hora, y=perdasQ[0])])
for i in range(1,nBranch):
    fig_perdasReativas.add_trace(go.Scatter(name = "Ramo {}".format(i+1),x=hora, y=perdasQ[i]))

fig_perdasReativas.update_layout(legend_valign="middle")


fig_perdasReativasControle = go.Figure(data=[go.Scatter(name="Ramo {}".format(1),x=hora, y=perdasQControle[0])])
for i in range(1,nBranch):
    fig_perdasReativasControle.add_trace(go.Scatter(name = "Ramo {}".format(i+1),x=hora, y=perdasQControle[i]))

fig_perdasReativasControle.update_layout(legend_valign="middle")


layout = html.Div(children=[

    #===========================================================================================
    #Data without control
    #===========================================================================================
    #------------------------------------------------------------------------------------------
    #Grafico de Perdas Ativas
    html.Div([
        html.H1(children='Dados de Trecho - Sem Controle',className='titulo_secao'),
    ],className='div_titulo_secao'),


    html.Div([
        html.Div([
            html.P('Perdas Ativas por Ramo [p.u.]'),
            
            dcc.Graph(
                id='grafico_perdasAtivas',
                figure=fig_perdasAtivas
            )
        ],id="wideGraph_yellow"),
    ]),

    #------------------------------------------------------------------------------------------
    #Analise de Perdas Ativas
        html.Div([

        html.Div([
            html.P('Máxima Perda'),
            html.H1(children="{:.3f} [p.u.]".format(maxPerdaP),id="id_maxPerdaP"),
         ],id="halfGraph_yellow"),


          html.Div([
            html.P('Mínima Perda'),
            html.H1(children="{:.3f} [p.u.]".format(minPerdaP),id="id_minPerdaP"),
            ],id="halfGraph_red"), 

            html.Div([
            html.P('Máxima Perda Total'),
            html.H1(children="{:.3f} [p.u.]".format(perdasP_maxTotal),id="id_maxPerdaPTotal"),
            ],id="halfGraph_green"), 
    ],className="halfDivConfig"),
    
    #------------------------------------------------------------------------------------------
    #Grafico de Perdas Reativas

    html.Div([
        html.Div([
            html.P('Perdas Reativas por Ramo [p.u.]'),
            
            dcc.Graph(
                id='grafico_perdasReativas',
                figure=fig_perdasReativas
            )
        ],id="wideGraph_red"),]),

    #===========================================================================================
    #Data with control
    #===========================================================================================
    #------------------------------------------------------------------------------------------
    #Grafico de Perdas Ativas
    html.Div([
        html.H1(children='Dados de Trecho - Controle Local Clássico',className='titulo_secao'),
    ],className='div_titulo_secao'),


    html.Div([
        html.Div([
            html.P('Perdas Ativas por Ramo [p.u.]'),
            
            dcc.Graph(
                id='grafico_perdasAtivas',
                figure=fig_perdasAtivasControle
            )
        ],id="wideGraph_yellow"),
    ]),

    #------------------------------------------------------------------------------------------
    #Analise de Perdas Ativas
        html.Div([

        html.Div([
            html.P('Máxima Perda'),
            html.H1(children="{:.3f} [p.u.]".format(maxPerdaPControle),id="id_maxPerdaP"),
         ],id="halfGraph_yellow"),


          html.Div([
           html.P('Redução Perdas Ativas'),
            html.H1(children="{:.2f} %".format(reducaoPerdasP),id="id_minPerdaP",style={'margin-left':'1.2em'}),
            ],id="halfGraph_red"), 

            html.Div([
            html.P('Máxima Perda Total'),
            html.H1(children="{:.3f} [p.u.]".format(perdasPControle_maxTotal),id="id_maxPerdaPTotal"),
            ],id="halfGraph_green"), 
    ],className="halfDivConfig"),
    
    #------------------------------------------------------------------------------------------
    #Grafico de Perdas Reativas

    html.Div([
        html.Div([
            html.P('Perdas Reativas por Ramo [p.u.]'),
            
            dcc.Graph(
                id='grafico_perdasReativas',
                figure=fig_perdasReativasControle
            )
        ],id="wideGraph_red"),])

],className="bodyContent")
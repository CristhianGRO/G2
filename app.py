from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import math
import dash

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


app = Dash(__name__, use_pages=True)
server = app.server

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
})

idBranch = []
for i in range(1,nBranch+1,1):
    idBranch.append("{}".format(i))
idBranch = idBranch*24


dfBranch = pd.DataFrame({
    "Id": idBranch,
    "Perdas_Ativas": perdasAtivas,
    "Perdas_Reativas": perdasReativas
})
   



#===========================================================================================
#Making the voltage Vector used to construct the voltage figure
#===========================================================================================
tensoes = []
for i in range(1,nBus+1,1):
    newdf = df.query('Id == "{}"'.format(i))
    tensaoAtual = newdf["Tensao"].tolist()
    tensoes.append(tensaoAtual)
#===========================================================================================
#Making the angle Vector used to construct the angle figure
#===========================================================================================
angulos = []
for i in range(1,nBus+1,1):
    newdf = df.query('Id == "{}"'.format(i))
    angAtual = newdf["Angulo"].tolist()
    angulos.append(angAtual)
#===========================================================================================
#Making the active loses Vector used to construct the angle figure
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



#===========================================================================================
#Making some Analysis
#===========================================================================================
#Voltage Analysis
maxTensaoHoraria = max(tensoes)
maxTensao = max(maxTensaoHoraria)
horaPico_inf = maxTensaoHoraria.index(maxTensao) + 1


minTensaoHoraria = min(tensoes)
minTensao = min(minTensaoHoraria)
horaPico_sup = minTensaoHoraria.index(min(minTensaoHoraria)) + 1

#Losses Analysis
maxPerdaPHoraria = max(perdasP)
maxPerdaP = max(maxPerdaPHoraria)

#Searching for the maximal total loss
perdasP_maxTotal = 0
for i in range(24):
    somaPerdaPHora = 0;
    for j in range(nBranch):
        somaPerdaPHora += perdasP[j][i]
    if(somaPerdaPHora>perdasP_maxTotal):
        perdasP_maxTotal = somaPerdaPHora
    



minPerdaPHoraria = min(perdasP)
minPerdaP = min(minPerdaPHoraria)




#https://plotly.com/python/reference/layout/

#===========================================================================================
#Making the voltage Figure
#===========================================================================================
fig_tensao = go.Figure(data=[go.Scatter(name="Barra {}".format(1),x=hora, y=tensoes[0])])
for i in range(1,nBus):
    fig_tensao.add_trace(go.Scatter(name = "Barra {}".format(i+1),x=hora, y=tensoes[i]))

fig_tensao.update_layout(legend_valign="middle")

#===========================================================================================
#Making the angle Figure
#===========================================================================================
fig_angulo = go.Figure(data=[go.Scatter(name="Barra {}".format(1),x=hora, y=angulos[0])])
for i in range(1,nBus):
    fig_angulo.add_trace(go.Scatter(name = "Barra {}".format(i+1),x=hora, y=angulos[i]))

fig_angulo.update_layout(legend_valign="middle")
#===========================================================================================
#Making the active Loss Figure
#===========================================================================================
fig_perdasAtivas = go.Figure(data=[go.Scatter(name="Ramo {}".format(1),x=hora, y=perdasP[0])])
for i in range(1,nBranch):
    fig_perdasAtivas.add_trace(go.Scatter(name = "Ramo {}".format(i+1),x=hora, y=perdasP[i]))

fig_perdasAtivas.update_layout(legend_valign="middle")

#===========================================================================================
#Making the reactive Loss Figure
#===========================================================================================
fig_perdasReativas = go.Figure(data=[go.Scatter(name="Ramo {}".format(1),x=hora, y=perdasQ[0])])
for i in range(1,nBranch):
    fig_perdasReativas.add_trace(go.Scatter(name = "Ramo {}".format(i+1),x=hora, y=perdasQ[i]))

fig_perdasReativas.update_layout(legend_valign="middle")


#https://plotly.com/python/reference/layout/



#Icons reference: https://fontawesome.com/icons


app.layout = html.Div(children=[
   
    #------------------------------------------------------------------------------------------
    #SuperiorBar
    html.Div([
        html.H1(children='G2 - Graph Generator'),
       
        html.H2(children='Automatic Visualization of Power Flow Data',className="subtitulo"),
        
    ],className="superiorBar"),

   #------------------------------------------------------------------------------------------
    #SideBar
    html.Div([
        html.Div([
            html.Img(src="../assets/imagens/profile.jpg"),
            html.H3(children='Oliveira, C. G. R.'),
            html.P(children='Pesquisador - UFMT'),
            html.Hr(className="HrSide"),
        ],className="profile"),


     html.Div([
            html.Div([
                dcc.Link(
                    f"{page['name']}", href=page["relative_path"]
                )
        ])
            for page in dash.page_registry.values()
            
        ],className="MenuLateral"
    ),

    ],className = "sideBar"),

	dash.page_container ,
    
                            
   
])


if __name__ == '__main__':
    app.run_server(debug=True,use_reloader=False)

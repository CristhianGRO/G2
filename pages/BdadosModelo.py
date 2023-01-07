from dash import Dash, html, dcc
import pandas as pd
import plotly.graph_objs as go
import dash

#Importing model variables avaiable from pages dadosLinha and dadosBarra
import pages.EdadosLinha as dadosLinha
import pages.DdadosBarra as dadosBarra

dash.register_page(
    __name__,
    title = 'Dados do Modelo',
    name  = 'Dados do Modelo'
)



barraPhotovoltaic = []
dadosGeracao = []
Ppico = []
#===========================================================================================
#Function that read the input data_Photovoltaic file
#===========================================================================================
def readInputPhotovoltaic():
    dataFile = open("data_Photovoltaic.txt","r")
    linhas = dataFile.readlines()
    j=0
    for linha in linhas:
        if j != 0:
            Barra = linha.split(" ",2)[0]
            Ppicoj = float(linha.split(" ",2)[1])
            for i in range(24):
                barraPhotovoltaic.append(Barra)
                Ppico.append(Ppicoj)
                geradoHora = float(linha.split(" ",27)[i+2])
                dadosGeracao.append(geradoHora)  
        else:
            nPhotovoltaic=int(linha.split(",",2)[0])
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
            for i in range(24):
                barraLoadCurve.append(Barra)
                loadCurveHora = float(linha.split(" ",27)[i+1])
                dadosLoadCurve.append(loadCurveHora)  
        else:
            nLoadCurve=int(linha.split(",",2)[0])
        j=j+1
    return nLoadCurve

nLoadCurve = readInputLoadCurve()


horaFV=[]
horaLC = []
ihora = 1

for j in range(24):
    horaFV.append(ihora)
    horaLC.append(ihora)
    ihora = ihora+1

if nPhotovoltaic > 1:
    horaFV   *= nPhotovoltaic
if nLoadCurve > 1:
    horaLC *= nLoadCurve

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

for i in range(nPhotovoltaic):
    newdfSolar = dfPhotovoltaic.query('Barra == "{}"'.format(barraPhotovoltaic[i+23]))
    newdfSolar['Phoraria'] = newdfSolar.Geracao_Horaria * newdfSolar.Potencia_Pico
    geracaoHorariaAtual = newdfSolar['Phoraria'].tolist()
    geracaoHoraria.append(geracaoHorariaAtual)

#===========================================================================================
#Making the hour load curve Vector used to construct the load curve figure
#===========================================================================================
curvaDeCargaHoraria = []

for i in range(nLoadCurve):
    newdfLoadCurve = dfLoadCurve.query('Barra == "{}"'.format(barraLoadCurve[i+23]))
    curvaDeCargaAtual = newdfLoadCurve["Curva_de_Carga"].tolist()
    curvaDeCargaHoraria.append(curvaDeCargaAtual)



#===========================================================================================
#Making the hour generation Figure
#===========================================================================================
fig_geracaoSolar = go.Figure(data=[go.Scatter(name="Barra de Geração: {}".format(barraPhotovoltaic[0][0]),x=horaFV, y=geracaoHoraria[0])])
for i in range(1,nPhotovoltaic):
    fig_geracaoSolar.add_trace(go.Scatter(name = "Barra de Geração: {}".format(barraPhotovoltaic[i+23][0]),x=horaFV, y=geracaoHoraria[i]))

fig_geracaoSolar.update_layout(legend_valign="middle")



#===========================================================================================
#Making the hour load Curve Figure
#===========================================================================================
fig_loadCurve = go.Figure(data=[go.Scatter(name="Barra de Carga: {}".format(barraLoadCurve[0]),x=horaLC, y=curvaDeCargaHoraria[0])])
for i in range(1,nLoadCurve):
    fig_loadCurve.add_trace(go.Scatter(name = "Barra de Carga: {}".format(barraLoadCurve[i+23]),x=horaLC, y=curvaDeCargaHoraria[i]))

fig_loadCurve.update_layout(legend_valign="middle")



#===========================================================================================
#Making some Analysis
#===========================================================================================
#Getting the total Load of the model
totalMW = 0
totalMVar = 0

for i in range(dadosBarra.nBus):
    totalMW   += float(dadosBarra.dataBus[i][2])
    totalMVar += float(dadosBarra.dataBus[i][3]) 

layout = html.Div(children=[
    
    
     html.Div([
            html.H1(children='Dados do Modelo',className='titulo_secao'),
        ],className='div_titulo_secao'),


        #------------------------------------------------------------------------------------------
        #Analise de Modelo
        html.Div([
            html.Div([
                html.P('Número de Barras'),
                html.H1(children="{}".format(dadosBarra.nBus),id="id_nBus",style={'margin-left':'2.5em'}),
            ],id="halfGraph_green"),

            html.Div([
                html.P('Número de Linhas'),
                html.H1(children="{}".format(dadosLinha.nBranch),id="id_nBranch",style={'margin-left':'2.5em'}),
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

       

   
],className="bodyContent")

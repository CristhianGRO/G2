from dash import Dash, html, dcc
import dash


app = Dash(__name__, use_pages=True)
server = app.server


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
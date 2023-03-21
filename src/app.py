import pandas as pd
import dash
from dash import dash, html, dcc, dash_table, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import numpy as np
from PIL import Image


            
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# add pic
#image_path = 'assets/dash_vanhouses.jpg'
pil_img = Image.open('assets/dash_vanhouses.jpg')





# load data (importing csv into pandas)
df_original = pd.read_csv('df_sampled.csv')

# dropdown selections
zoning_classification = np.sort(df_original["zoning_classification"].unique())
geo_local_area_list = np.sort(df_original["Geo Local Area"].unique())
year = np.sort(df_original["report_year"].unique())

#cards
card_main = dbc.Card(
    [
        dbc.CardImg(src=pil_img, top=True, bottom=False, style={'height':'60%'}),
        dbc.CardBody(
            [
                html.H1("Vancouver Housing Market", className="card-title"),
                #html.H6("Lesson 1:", className="card-subtitle"),
                html.P(
                    "Our Python-based dashboard application gives an easy way for people to explore housing prices in Vancouver city.",
                    className="card-text",
                ),
                
            ]
        ),
    ],
    color="light",   
    style={"height": 380},
    #inverse=True,   # change color of text (black or white)
    outline=False,  # True = remove the block colors from the background and header
)

card_dd = dbc.Card(
    dbc.CardBody(
            [#1st Dropdown selection for "report_year"
                html.H6("Year Reported"),
                dcc.Dropdown(id = "report_year",
                            value = 2022,
                            clearable = False, 
                            multi = False,
                            options=[{'label': x, 'value': x} for x in year],
                            style = {'width': "35%"}),
                html.Br(),
                html.Br(),

                #2nd Dropdown selection for "geo_local_area"
                html.H6("Neigborhood"),
                dcc.Dropdown(id = "geo_local_area",
                            value = ["Fairview","Downtown"],
                            #clearable = False, 
                            multi =True,
                            options=[{'label': x, 'value': x} for x in geo_local_area_list],
                            style = {'width': "100%"}),
                html.Br(),
                html.Br(),

                #3rd Dropdown selection for "zoning_classification"
                html.H6("Type of the Property"),
                dcc.Dropdown(id = "zoning_classification",
                            value = ["Commercial","Historical Area"],
                            #clearable = False, 
                            multi =True,
                            options=[{'label': x, 'value': x} for x in zoning_classification],
                            style = {'width': "100%"}),
                
            ]),
            style={"height": 380}
)

#App layout
app.layout = html.Div([  

     dbc.Row([dbc.Col(card_main, width =5),
             dbc.Col(card_dd, width =5)], justify="around"),

    
    html.Br(),
    html.Br(),

    dbc.Row([
    html.H5('Distribution of Housing Prices'),
            dcc.Graph(id="his_housing_price")]),

    dbc.Row([
        dbc.Col([
            html.H5('Bubble Chart of Housing Prices by Legal Type'),
            dcc.Graph(id="bc_housing_price")
        ]),

        dbc.Col([
            html.H5('Total Amount of houses in Different Neighborhood'),
            dcc.Graph(id="pc_housing_price")
    
        ])
        
    ])
]
    ,style={'padding': 40})





# Connect plots with Dash components
@app.callback(
    Output("his_housing_price", "figure"),
    Output("bc_housing_price", "figure"),
    Output("pc_housing_price", "figure"),
    Input("report_year", "value"),
    Input("geo_local_area", "value"),
    Input("zoning_classification", "value")
)
def housing_price_histogram(year_slcted, neighborhood_slcted, type_property_slcted):
    
    #filter data based on user input
    df = df_original.copy()
    df = df[df['report_year'] == year_slcted]
    df = df[df["Geo Local Area"].isin(neighborhood_slcted)]
    df = df[df["zoning_classification"].isin(type_property_slcted)]
    # df = df[(df['Geo Local Area'] == neighborhood_slcted ) & (df['zoning_classification'] == type_property_slcted)]
    #dff = dff[dff['zoning_classification'] == type_property_slcted]
    
    #plot distribution of housing prices
    his = px.histogram(
        df, nbins=40,
        x="current_land_value")
    his.update_traces(marker=dict(line=dict(width=1, color="white")))
    his.update_layout(
    xaxis_title_text='House Prices ($)', # xaxis label
    yaxis_title_text='Number of Houses', # yaxis label
    bargap=0.1)

    bc = px.scatter(df, 
                    x="Geo Local Area",
                    y="current_land_value",
                    color="legal_type", 
                    size="current_land_value",
                    hover_name="year_built", 
                    log_x=False, 
                    size_max=40,
                    labels={"Geo Local Area": "Neighborhood", 
                            "current_land_value": "House Prices ($)"})
    #bc.update_layout(height=800, width=500)
    
    df_pc = df["Geo Local Area"].value_counts()
    pc = px.pie(df_pc, values = df_pc.values, names = df_pc.index, color = "Geo Local Area")



    return his, bc, pc




if __name__ == '__main__':
    app.run_server(debug=True)
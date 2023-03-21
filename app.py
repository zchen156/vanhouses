import pandas as pd
import plotly.graph_objs as go
import dash
from dash import dash, html, dcc, dash_table, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt

            
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# Load data (importing csv into pandas)
df_original = pd.read_csv('df_sampled.csv')

# dropdown selections
zoning_classification = np.sort(df_original["zoning_classification"].unique())
geo_local_area_list = np.sort(df_original["Geo Local Area"].unique())
year = np.sort(df_original["report_year"].unique())

#App layout
app.layout = dbc.Container([
    
    #App title
    html.H1("Vancouver Housing Market", style = {'text-align': 'left'}),
    html.Br(),
    
    #Dropdown layout
    dbc.Row([
        dbc.Col([
    
    #1st Dropdown selection for "report_year"
    html.H6("Year Reported"),
    dcc.Dropdown(id = "report_year",
                 value = 2022,
                 clearable = False, 
                 multi = False,
                 options=[{'label': x, 'value': x} for x in year],
                 style = {'width': "35%"}),
    html.Br(),

    #2nd Dropdown selection for "geo_local_area"
    html.H6("Neigborhood"),
    dcc.Dropdown(id = "geo_local_area",
                 value = ["Fairview","Downtown"],
                 #clearable = False, 
                 multi =True,
                 options=[{'label': x, 'value': x} for x in geo_local_area_list],
                 style = {'width': "50%"}),
    html.Br(),

    #3rd Dropdown selection for "zoning_classification"
    html.H6("Type of the Property"),
    dcc.Dropdown(id = "zoning_classification",
                 value = ["Commercial","Historical Area"],
                 #clearable = False, 
                 multi =True,
                 options=[{'label': x, 'value': x} for x in zoning_classification],
                 style = {'width': "50%"}),
    
                 ])
    
]),


    
html.Br(),
html.H5('Distribution of Housing Prices'),
dcc.Graph(id="his_housing_price"),

html.Br(),
html.H5('Bubble Chart of Housing Prices by Legal Type'),
dcc.Graph(id="bb_housing_price")
])


# Connect plots with Dash components
@app.callback(
    Output("his_housing_price", "figure"),
    Output("bb_housing_price", "figure"),
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
    bc.update_layout(height=800, width=500)
    
    return his, bc




if __name__ == '__main__':
    app.run_server(debug=True)
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px


app = dash.Dash(__name__)


app.layout = html.Div(children=[
    html.H1("Dropdown Check", style={"text-align":"center"}),
    dcc.Dropdown(options=[
        {"label":"All Sites", "value":"All"},
        {'label': 'CCAFS LC-40', 'value': "CCAFS LC-40"},
        {"label": "VAFB SLC-4E", "value" : "VAFB SLC-4E"},
        {"label" : "KSC LC-39A", "value" : "KSC LC-39A"},
        {"label" : "CCAFS SLC-40", "value" : "CCAFS SLC-40"}
    ], value="All", searchable=True, placeholder="Choose Launch Sites")

])



if __name__ == "__main__":
    app.run_server(port=3000, host="localhost", debug=True)
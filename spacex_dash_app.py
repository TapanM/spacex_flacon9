# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id="site-dropdown", options=[
                                    {"label":"All Sites", "value":"ALL"},
                                    {'label': 'CCAFS LC-40', 'value': "CCAFS LC-40"},
                                    {"label": "VAFB SLC-4E", "value" : "VAFB SLC-4E"},
                                    {"label" : "KSC LC-39A", "value" : "KSC LC-39A"},
                                    {"label" : "CCAFS SLC-40", "value" : "CCAFS SLC-40"}
                                ], value="ALL", searchable=True, placeholder="Choose Launch Sites"),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min = 0, max = 10000, step = 1000,
                                                marks={
                                                    0: '0',
                                                    2500 : '2500',
                                                    5000 : '5000',
                                                    7500 : '7500',
                                                    10000 : '10000'
                                                },
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

filterd_df = spacex_df[spacex_df['class']==1].groupby("Launch Site", as_index=False)["class"].count()
fd = spacex_df.groupby(["Launch Site", "class"], as_index=False)["class"].count()

def compute_dataframe(label):
    return fd[fd["Launch Site"] == label]

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(data_frame=filterd_df, values="class", title="Total Success Launch By Site", names='Launch Site')
    else:
        temp = spacex_df[spacex_df["Launch Site"] == entered_site].groupby("class", as_index=False)["Launch Site"].count()
        fig = px.pie(data_frame=temp, values="Launch Site", title="Success and Failure rate of {entered_site}".format(entered_site=entered_site),names="class")
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
               Input(component_id="payload-slider", component_property='value')])

def get_scatter_chart(entered_site, mass_payload):
    if entered_site == "ALL":
        fig = px.scatter(data_frame=spacex_df, x="Payload Mass (kg)", y="class", color="Booster Version Category")
    else:
        spacex_filter = spacex_df[(spacex_df["Launch Site"] == entered_site) & (spacex_df["Payload Mass (kg)"] >= mass_payload[0]) & (spacex_df["Payload Mass (kg)"] <= mass_payload[1])][["Payload Mass (kg)", "class", "Booster Version Category"]]
        fig = px.scatter(data_frame=spacex_filter, x="Payload Mass (kg)", y="class", color="Booster Version Category")
    return fig
# Run the app
if __name__ == "__main__":
    app.run_server(port=3000, host="localhost", debug=True)
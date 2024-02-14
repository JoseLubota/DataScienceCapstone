# Import required libraries
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px


url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
# Read the airline data into pandas dataframe
spacex_df =  pd.read_csv(url)

# Create a dash application
app = dash.Dash(__name__)

# Build dash app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard', 
                                style={'textAlign': 'center', 'color': '#503D36',
                                'font-size': 30}),

                               dcc.Dropdown(id='site-dropdown',
                                            options = [
                                                {'label': "All Sites", 'value': "All Sites"},
                                                *[{'label': site, 'value': site} for site in spacex_df["Launch Site"].unique()]
                                                ],
                                            placeholder = "All Sites",
                                               ),
                                html.Br(),
                                # Segment 1
                                html.Div([
                                        html.Div(dcc.Graph(id='success-pie-chart')),
                                ], style={'display': 'flex'}),
                                
                              
                                html.Br(),
                                # Segment 2
                                html.Div([
                                        dcc.RangeSlider(id ="payload-slider",
                                                        min=0, max=10000, step=1000,
                                                        marks = {0:'0', 100:'100'},
                                                        value = [0, 10000]
                                                        ),
                                                        
                                        html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ],style={'display': 'flex'}),
                        ])
                

 


# Callback decorator
@app.callback( 
               Output(component_id='success-pie-chart', component_property='figure'),
               Input(component_id='site-dropdown', component_property='value')
            )

# Computation to callback function and return graph
def get_pie_chart(entered_site):

    filtered_df = spacex_df
    if entered_site == "All Sites":
        fig = px.pie(filtered_df,
                     values ="class",
                     names = "Launch Site",
                     title="title",
                    )
        return fig
    else:
        filtered_df = spacex_df[spacex_df["Launch Site"] == entered_site]
        fig = px.pie(filtered_df,
                values ="class",
                names = "class",
                title=entered_site,
                )
        return fig
"""
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),

    [Input(component_id='site-dropdown', component_property='value'), 
     Input(component_id="payload-slider", component_property="value")]
)
def get_Scatter_plot(dropd, slider):
    if dropd == "All Sites":
        return
"""
# Run the app
if __name__ == '__main__':
    app.run_server(port = 8054)
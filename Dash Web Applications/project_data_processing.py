import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update

from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    us_states = json.load(response)


airline_data =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})


# Data for the Yearly Airline Performance Report
def performance_data(df):
    # Number of flights under different cancellation categories
    cancel_df = df[df['Cancelled'] > 0].copy()
    cancel_df = cancel_df.groupby(['CancellationCode'])['Cancelled'].sum().astype('int').reset_index()
    cancel_df.rename(columns={'Cancelled': 'Number of Cancellations', 'CancellationCode': 'Cancellation Code'},
                     inplace=True)
    # Average flight time by reporting airline
    ft_df = df[['Reporting_Airline', 'AirTime']].copy()
    ft_df = ft_df.groupby(['Reporting_Airline'])['AirTime'].mean().reset_index()
    ft_df.rename(columns={'AirTime': 'Avg Airtime'},
                 inplace=True)
    # % of diverted airport landings by reporting airline
    divert_df = df[['Reporting_Airline', 'Diverted']].copy()
    divert_df = divert_df.loc[(divert_df != 0).any(axis=1)]
    divert_df = divert_df.groupby(['Reporting_Airline'])['Diverted'].sum().astype('int').reset_index()
    # Number of flights from each state
    origin_df = df.groupby(['OriginState'])['Flights'].sum().reset_index()
    # Number of flights to each state by reporting airline
    dest_df = df[['Reporting_Airline', 'DestState']].copy()
    dest_df.loc[:, 'Total Flights'] = 1
    dest_df = dest_df.groupby(['DestState', 'Reporting_Airline'])['Total Flights'].count().reset_index()
    
    return [cancel_df, ft_df, divert_df, origin_df, dest_df]


def perf_graphs(df):
    # Compute required information for creating graph from the data
    cancel_df, ft_df, divert_df, origin_df, dest_df = performance_data(df)

    # Bar chart for cancellation data
    cancel_fig = px.bar(cancel_df, x='Number of Cancellations', y='Cancellation Code', title='Number of flight cancellations by cancellation code')
    # Line plot for average flight time by reporting airline
    ft_fig = px.line(ft_df, x='Reporting_Airline', y='Avg Airtime', title='Average airtime per flight (minutes) by reporting airline')
    # Pie plot for % of diverted airport landings by reporting airline
    divert_fig = px.pie(divert_df, values='Diverted', names='Reporting_Airline', title='Percent of diverted airport landings by reporting airline')
    # Choropleth map of flights from each state by reporting airline
    origin_fig = px.choropleth(origin_df, 
                               geojson=us_states, 
                               locations='OriginState', 
                               color='Flights',
                               locationmode = 'USA-states',
                               hover_data=['OriginState', 'Flights'], 
                               color_continuous_scale='GnBu',
                               range_color=[0, origin_df['Flights'].max()])
    origin_fig.update_layout(title_text='Number of flights from each US state',
                             geo_scope='usa')
    # Treemap of flights to each state by reporting airline
    dest_fig = px.treemap(dest_df, 
                          path=[px.Constant('United States'), 'DestState', 'Reporting_Airline'], 
                          values='Total Flights')
    dest_fig.update_layout(title='Flights to each state by reporting airline')

    return dest_fig


pd.set_option('display.max_columns', None)
perf_graphs(airline_data)

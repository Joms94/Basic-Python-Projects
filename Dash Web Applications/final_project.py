import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px


# Components for the choropleth map
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    us_states = json.load(response)


app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True


airline_data =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})

year_list = [i for i in range(2005, 2021, 1)]


app.layout = html.Div(children=[html.H1('US Domestic Airline Flights Performance',
                                         style={'text-align': 'center', 'color': '#503D36', 'font-size': 35}),
                                html.Br(),
                                # Select report type
                                html.Div([
                                    html.Div([
                                        html.H2('Report type: ',
                                                style={'font-size': 20, 'color': '#503D36', 'margin-right': '2em', 'justify-content': 'center'}),
                                        html.Div(dcc.Dropdown(id='report-input',
                                                              options=[{'label': 'Yearly Airline Performance Report', 'value': 'perf-rep'},
                                                                    {'label': 'Yearly Airline Delay Report', 'value': 'delay-rep'}],
                                                              placeholder='Select a report',
                                                              style={'width': 290, 'padding': '3px', 'font-size': '20px', 'text-align-last': 'center'}))],
                                            style={'display': 'flex', 'justify-content': 'center'}),
                                    # Choose year
                                    html.Div([
                                        html.H2('Choose year: ',
                                                style={'font-size': 20, 'color': '#503D36', 'margin-right': '2em', 'justify-content': 'center'}),
                                        html.Div(dcc.Dropdown(id='year-input',
                                                              options=[{'label': i, 'value': i} for i in year_list],
                                                              placeholder='Select a year',
                                                              style={'width': 290, 'padding': '3px', 'font-size': '20px', 'text-align-last': 'center'}))],
                                            style={'display': 'flex', 'justify-content': 'center'})]),
                                html.Br(),
                                html.Div(
                                    # Plotting number of flights as a bar plot
                                    [], id='plot-1',
                                    style={'display': 'flex', 'justify-content': 'center'}),
                                html.Div([
                                    # Avg flight time as line; % flights diverted as pie
                                    html.Div([], id='plot-2'),
                                    html.Div([], id='plot-3')],
                                    style={'display': 'flex', 'justify-content': 'center'}),
                                html.Div([
                                    # No. flights from each state as choropleth; no. flights to each state as treemap
                                    html.Div([], id='plot-4'),
                                    html.Div([], id='plot-5')],
                                    style={'display': 'flex', 'justify-content': 'center'})
                                ]
                            )


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
    divert_df = df[df['DivAirportLandings'] != 0.0]
    # Number of flights from each state
    origin_df = df.groupby(['OriginState'])['Flights'].sum().reset_index()
    # Number of flights to each state by reporting airline
    dest_df = df[['Reporting_Airline', 'DestState']].copy()
    dest_df.loc[:, 'Total Flights'] = 1
    dest_df = dest_df.groupby(['DestState', 'Reporting_Airline'])['Total Flights'].count().reset_index()
    
    return cancel_df, ft_df, divert_df, origin_df, dest_df


# Data for the Yearly Airline Delay Report
def delay_data(df):
    # Monthly average carrier delay
    avg_car = df.groupby(['Month','Reporting_Airline'])['CarrierDelay'].mean().reset_index()
    # Monthly average weather delay
    avg_weather = df.groupby(['Month','Reporting_Airline'])['WeatherDelay'].mean().reset_index()
    # Monthly average national air system delay
    avg_NAS = df.groupby(['Month','Reporting_Airline'])['NASDelay'].mean().reset_index()
    # Monthly average security delay
    avg_sec = df.groupby(['Month','Reporting_Airline'])['SecurityDelay'].mean().reset_index()
    # Monthly average late aircraft delay
    avg_late = df.groupby(['Month','Reporting_Airline'])['LateAircraftDelay'].mean().reset_index()

    return avg_car, avg_weather, avg_NAS, avg_sec, avg_late


@app.callback([Output(component_id='plot-1', component_property='children'),
               Output(component_id='plot-2', component_property='children'),
               Output(component_id='plot-3', component_property='children'),
               Output(component_id='plot-4', component_property='children'),
               Output(component_id='plot-5', component_property='children')
                ],
              [Input(component_id='report-input', component_property='value'),
               Input(component_id='year-input', component_property='value')],
              [State("plot-1", 'children'), State("plot-2", "children"),
               State("plot-3", "children"), State("plot-4", "children"),
               State("plot-5", "children")
               ])
def select_report(report_type, year_input, c1, c2, c3, c4, c5):
    df = airline_data[airline_data['Year']==year_input]
    
    if report_type == 'perf-rep':
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

        return [dcc.Graph(figure=cancel_fig), 
                dcc.Graph(figure=ft_fig), 
                dcc.Graph(figure=divert_fig), 
                dcc.Graph(figure=origin_fig), 
                dcc.Graph(figure=dest_fig)]


    else:
        # Compute required information for creating graph from the data
        avg_car, avg_weather, avg_NAS, avg_sec, avg_late = delay_data(df)

        # Line plot for carrier delay
        carrier_fig = px.line(avg_car, x='Month', y='CarrierDelay', color='Reporting_Airline', title='Average carrier delay time (minutes) by airline')
        # Line plot for weather delay
        weather_fig = px.line(avg_weather, x='Month', y='WeatherDelay', color='Reporting_Airline', title='Average weather delay time (minutes) by airline')
        # Line plot for nas delay
        nas_fig = px.line(avg_NAS, x='Month', y='NASDelay', color='Reporting_Airline', title='Average NAS delay time (minutes) by airline')
        # Line plot for security delay
        sec_fig = px.line(avg_sec, x='Month', y='SecurityDelay', color='Reporting_Airline', title='Average security delay time (minutes) by airline')
        # Line plot for late aircraft delay
        late_fig = px.line(avg_late, x='Month', y='LateAircraftDelay', color='Reporting_Airline', title='Average late aircraft delay (minutes) by airline')

        return [dcc.Graph(figure=carrier_fig), 
                dcc.Graph(figure=weather_fig), 
                dcc.Graph(figure=nas_fig), 
                dcc.Graph(figure=sec_fig), 
                dcc.Graph(figure=late_fig)]


if __name__ == '__main__':
    app.run_server(debug=False)

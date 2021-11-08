import pandas as pd
import plotly.express as px
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

if __name__ == '__main__':
    airline_data =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                                encoding = "ISO-8859-1",
                                dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                    'Div2Airport': str, 'Div2TailNum': str})

    # Randomly sample 500 data points. Setting the random state to be 42 so that we get same result.
    data = airline_data.sample(n=500, random_state=42)

    # Pie Chart Creation
    fig = px.pie(data, values='Flights', names='DistanceGroup', title='Distance group proportion by flights')


    app = dash.Dash(__name__)
    app.layout = html.Div(children=[html.H1('Airline Dashboard',
                                            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
                                    html.P('Proportion of distance group (250 mile distance interval group) by flights.', 
                                                style={'textAlign':'center', 'color': '#F57241'}),
                                    dcc.Graph(figure=fig)])


    @app.callback(
        Output(component_id='my-output', component_property='children'),
        Input(component_id='my-input', component_property='value'))
    def update_output_div(input_value):
        return 'Output: {}'.format(input_value)



    app.run_server()

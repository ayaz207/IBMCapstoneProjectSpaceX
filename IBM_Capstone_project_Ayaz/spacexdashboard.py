import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
names = spacex_df['Launch Site'].unique()
# Create a dash application
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                 {'label': 'All Sites', 'value': 'All'},
                                                 {'label': names[0], 'value': names[0]},
                                                 {'label': names[1], 'value': names[1]},
                                                 {'label': names[2], 'value': names[2]},
                                                 {'label': names[3], 'value': names[3]}
                                             ],
                                             value='All',
                                             placeholder="Select a Launch Site here",
                                             searchable=True,
                                             style={'width': '80%', 'padding': '3px', 'font-size': '20px',
                                                    'text-align-last': 'center'}),
                                html.Br(),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                # html.Div([ ], id='success-pie-chart'),
                                html.Br(),
                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                # dcc.RangeSlider(id='payload-slider',min = 0, max =10000, step = 1000, value = [min_payload,max_payload]),
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0,
                                    max=10000,
                                    step=1000,
                                    value=[spacex_df['Payload Mass (kg)'].min(), spacex_df['Payload Mass (kg)'].max()],
                                    marks={0: {'label': '0'}, 2500: {'label': '2500'}, 5000: {'label': '5000'},
                                           7500: {'label': '7500'}, 10000: {'label': '10000'}}
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_graph(entered_site):
    if entered_site == 'All':
        # Compute required information for creating graph from the data
        pie_fig = px.pie(spacex_df, values='class', names='Launch Site', title='Total Success Launches by site')
        return pie_fig
    else:
        # Select data
        df = spacex_df[0:0]
        df = df[['class']]
        df['class'] = df['class'].astype(int)
        list_rate = []
        for launch_site, rate in zip(spacex_df['Launch Site'], spacex_df['class']):
            if launch_site == entered_site:
                list_rate.append(rate)
        df['class'] = list_rate
        pie_fig = px.pie(df, names='class', title='Total Success Launches for site %s' % entered_site)
        return pie_fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')
               ])
def get_graph_load(entered_site, payload_range):
    # print("Payload: ",payload_range)
    if entered_site == 'All':
        print("IN IF")
        # Compute required information for creating graph from the data
        # df_new = spacex_df[0:0]
        # df_new= df_new[['class','Payload Mass (kg)']]
        # mass_load=[]
        # for i in range payload_range:

        # mass_load.append(i)
        # df['Payload Mass (kg)']=mass_load
        scatter_fig = px.scatter(spacex_df, x="Payload Mass (kg)", y="class", color='Booster Version Category',
                                 title='Correlation between Payload and Success for all Sites')
        return scatter_fig
    else:
        # Select data
        print("In ELSE")
        df = spacex_df[0:0]
        df = df[['class', 'Payload Mass (kg)', 'Booster Version Category']]
        df['class'] = df['class'].astype(int)
        list_rate = []
        mass_load = []
        color_list = []
        for launch_site, rate, mass, color in zip(spacex_df['Launch Site'], spacex_df['class'],
                                                  spacex_df['Payload Mass (kg)'],
                                                  spacex_df['Booster Version Category']):
            if launch_site == entered_site:
                list_rate.append(rate)
                mass_load.append(mass)
                color_list.append(color)
                # df['Payload Mass (kg)'].append(mass)
        df['class'] = list_rate
        df['Payload Mass (kg)'] = mass_load
        df['Booster Version Category'] = color_list
        scatter_fig = px.scatter(df, x="Payload Mass (kg)", y="class", color='Booster Version Category',
                                 title='Correlation between Payload and Success for site %s' % entered_site)
        return scatter_fig


# Run the app
if __name__ == '__main__':
    app.run_server()

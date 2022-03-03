# Import required libraries
from turtle import width
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
sites = spacex_df['Launch Site'].unique()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36',
                   'font-size': 50}),

    # TASK 1: Add a dropdown list to enable Launch Site selection
    # The default select value is for ALL sites
    dcc.Dropdown(id='site-dropdown',
                 options=[
                     {'label': 'All sites', 'value': 'ALL'},
                     {'label': sites[0], 'value': sites[0]},
                     {'label': sites[1], 'value': sites[1]},
                     {'label': sites[2], 'value': sites[2]},
                     {'label': sites[3], 'value': sites[3]},
                 ],
                 value='ALL',
                 placeholder='Site selection',
                 optionHeight=50,
                 style={'font-size': 30, 'height': 50,
                        'vertical-align': 'center'},
                 searchable=True),

    html.Br(),

    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    # If a specific launch site was selected, show the Success vs. Failed counts for the site
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload Range (Kg):", style={'font-size': 30}),
    # TASK 3: Add a slider to select payload range
    dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000,
                    value=[min_payload, max_payload],
                    marks={
                        0: {'label': '0', 'style': {'font-size': 25}},
                        1000: {'label': '1K', 'style': {'font-size': 25}},
                        2000: {'label': '2K', 'style': {'font-size': 25}},
                        3000: {'label': '3K', 'style': {'font-size': 25}},
                        4000: {'label': '4K', 'style': {'font-size': 25}},
                        5000: {'label': '5K', 'style': {'font-size': 25}},
                        6000: {'label': '6K', 'style': {'font-size': 25}},
                        7000: {'label': '7K', 'style': {'font-size': 25}},
                        8000: {'label': '8K', 'style': {'font-size': 25}},
                        9000: {'label': '9K', 'style': {'font-size': 25}},
                        10000: {'label': '10K', 'style': {'font-size': 25}}
                    }),
    html.Br(),

    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),

])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


@app.callback(
    [
        Output(component_id='success-pie-chart', component_property='figure'),
        Output(component_id='success-payload-scatter-chart',
               component_property='figure')
    ],
    [
        Input(component_id='site-dropdown', component_property='value'),
        # Input(component_id='payload-slider', component_property='value')
    ]
)
def get_charts(entered_site):
    success_launched = spacex_df[['Launch Site', 'class']].groupby(
        'Launch Site').sum('class')
    success_launched.reset_index(inplace=True)
    filter_site = spacex_df[spacex_df['Launch Site'] == entered_site]
    label1 = 'Total Success Launched for site ' + entered_site
    label2 = 'Correlation between Payload and Success for site ' + entered_site

    if entered_site == 'ALL':
        pie_fig = px.pie(success_launched, values='class', names='Launch Site',
                         title='Total Success Launched by Site',
                         height=600)
        pie_fig.update_layout(font_size=26)

        scatter_fig = px.scatter(spacex_df, x='Payload Mass (kg)', y='class',
                                 color='Booster Version Category', height=800,
                                 title='Correlation between Payload and Success for all sites')
        scatter_fig.update_traces(marker_size=18)
        scatter_fig.update_layout(font_size=26)

    else:
        pie_fig = px.pie(filter_site, names='class', title=label1,
                         height=600)
        pie_fig.update_layout(font_size=26)

        scatter_fig = px.scatter(filter_site, x='Payload Mass (kg)', y='class',
                                 color='Booster Version Category', height=800,
                                 title=label2)
        scatter_fig.update_traces(marker_size=18)
        scatter_fig.update_layout(font_size=26)

    return[pie_fig, scatter_fig]


# Run the app
if __name__ == '__main__':
    app.run_server()

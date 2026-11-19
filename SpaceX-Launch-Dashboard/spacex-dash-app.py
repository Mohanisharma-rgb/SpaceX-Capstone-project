#!/usr/bin/env python
# coding: utf-8

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load SpaceX dataset
spacex_df = pd.read_csv('spacex_launch_dash.csv')

# Find minimum and maximum payload
min_payload = spacex_df['Payload Mass (kg)'].min()
max_payload = spacex_df['Payload Mass (kg)'].max()

# Initialize Dash application
app = dash.Dash(__name__)

app.title = "SpaceX Launch Records Dashboard"

# Create dashboard layout
app.layout = html.Div(children=[

    # Dashboard Title
    html.H1(
        'SpaceX Launch Records Dashboard',
        style={
            'textAlign': 'center',
            'color': '#503D36',
            'font-size': 40
        }
    ),

    # TASK 1: Launch Site Dropdown
    html.Div([
        html.Label("Select Launch Site:"),

        dcc.Dropdown(
            id='site-dropdown',
            options=[
                {'label': 'All Sites', 'value': 'ALL'}
            ] + [
                {'label': site, 'value': site}
                for site in spacex_df['Launch Site'].unique()
            ],
            value='ALL',
            placeholder="Select a Launch Site here",
            searchable=True
        )
    ], style={'width': '80%', 'margin': 'auto'}),

    html.Br(),

    # TASK 2: Success Pie Chart
    html.Div(
        dcc.Graph(id='success-pie-chart')
    ),

    html.Br(),

    # TASK 3: Payload Range Slider
    html.Div([
        html.Label("Select Payload Range (Kg):"),

        dcc.RangeSlider(
            id='payload-slider',
            min=0,
            max=10000,
            step=1000,
            marks={
                0: '0',
                1000: '1000',
                2000: '2000',
                3000: '3000',
                4000: '4000',
                5000: '5000',
                6000: '6000',
                7000: '7000',
                8000: '8000',
                9000: '9000',
                10000: '10000'
            },
            value=[min_payload, max_payload]
        )
    ], style={'width': '80%', 'margin': 'auto'}),

    html.Br(),

    # TASK 4: Payload Success Scatter Chart
    html.Div(
        dcc.Graph(id='success-payload-scatter-chart')
    )

])


# TASK 2: Callback for Success Pie Chart
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)

def get_pie_chart(entered_site):

    if entered_site == 'ALL':

        success_data = spacex_df.groupby(
            'Launch Site'
        )['class'].sum().reset_index()

        fig = px.pie(
            success_data,
            values='class',
            names='Launch Site',
            title='Total Successful Launches by Launch Site'
        )

        return fig

    else:

        filtered_df = spacex_df[
            spacex_df['Launch Site'] == entered_site
        ]

        success_data = filtered_df['class'].value_counts().reset_index()

        success_data.columns = ['class', 'count']

        fig = px.pie(
            success_data,
            values='count',
            names='class',
            title='Launch Success and Failure for Site: ' + entered_site
        )

        return fig


# TASK 4: Callback for Payload Scatter Chart
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),

    [
        Input('site-dropdown', 'value'),
        Input('payload-slider', 'value')
    ]
)

def get_scatter_chart(entered_site, payload_range):

    low, high = payload_range

    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]

    if entered_site == 'ALL':

        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Correlation Between Payload and Launch Success'
        )

        return fig

    else:

        filtered_df = filtered_df[
            filtered_df['Launch Site'] == entered_site
        ]

        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Payload vs Launch Success for Site: ' + entered_site
        )

        return fig


# Run the application
if __name__ == '__main__':
    app.run(debug=True)
    
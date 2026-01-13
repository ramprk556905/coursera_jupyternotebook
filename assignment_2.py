#!/usr/bin/env python
# coding: utf-8

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the Automobile Sales data
data = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv'
)

# Initialize Dash app
app = dash.Dash(__name__)

# Dropdown options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

# List of Years
year_list = sorted(data['Year'].unique())

# App Layout
app.layout = html.Div([
    # TASK 2.1: Title
    html.H1("Automobile Sales Statistics Dashboard",
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 30}),
    
    # TASK 2.2: Dropdown Menus
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value='Yearly Statistics',
            placeholder='Select Statistics'
        )
    ]),

    html.Div(
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value=year_list[0]
        )
    ),

    # TASK 2.3: Output Container
    html.Div([
        html.Div(id='output-container', className='chart-grid', style={'display': 'flex'})
    ])
])

# =====================================================
# TASK 2.4: Callback to Enable/Disable Year Dropdown
# =====================================================
@app.callback(
    Output('select-year', 'disabled'),
    Input('dropdown-statistics', 'value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True


# =====================================================
# CALLBACK FOR OUTPUT PLOTS (TASK 2.5 & TASK 2.6)
# =====================================================
@app.callback(
    Output('output-container', 'children'),
    [Input('dropdown-statistics', 'value'),
     Input('select-year', 'value')]
)
def update_output_container(selected_statistics, input_year):

    # ======================================================
    # TASK 2.5: Recession Report
    # ======================================================
    if selected_statistics == 'Recession Period Statistics':

        recession_data = data[data['Recession'] == 1]

        # Plot 1 — Line Chart (Sales fluctuation)
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x='Year',
                y='Automobile_Sales',
                title="Average Automobile Sales During Recession"
            )
        )

        # Plot 2 — Avg Vehicles Sold by Type
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(
                average_sales,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title="Average Vehicles Sold by Type During Recession"
            )
        )

        # Plot 3 — Pie Chart (Expenditure Share)
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title="Advertising Expenditure Share by Vehicle Type During Recession"
            )
        )

        # Plot 4 — Unemployment vs Sales
        unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(
                unemp_data,
                x='unemployment_rate',
                y='Automobile_Sales',
                color='Vehicle_Type',
                title="Effect of Unemployment Rate on Vehicle Type and Sales"
            )
        )

        return [
            html.Div(className='chart-item',
                     children=[html.Div(R_chart1), html.Div(R_chart2)],
                     style={'display': 'flex'}),

            html.Div(className='chart-item',
                     children=[html.Div(R_chart3), html.Div(R_chart4)],
                     style={'display': 'flex'})
        ]

    # ======================================================
    # TASK 2.6: Yearly Report
    # ======================================================
    elif input_year and selected_statistics == 'Yearly Statistics':

        yearly_data = data[data['Year'] == input_year]

        # Plot 1 — Yearly Automobile Sales (overall)
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(
                yas,
                x='Year',
                y='Automobile_Sales',
                title="Yearly Automobile Sales (Overall)"
            )
        )

        # Plot 2 — Monthly Sales
        mas = data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(
                mas,
                x='Month',
                y='Automobile_Sales',
                title="Total Monthly Automobile Sales"
            )
        )

        # Plot 3 — Avg Vehicles Sold by Type
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title=f"Average Vehicles Sold by Vehicle Type in {input_year}"
            )
        )

        # Plot 4 — Advertisement Expenditure
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(
                exp_data,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title=f"Advertisement Expenditure by Vehicle Type in {input_year}"
            )
        )

        return [
            html.Div(
                className='chart-row',
                children=[
                    html.Div(Y_chart1, style={'width': '50%', 'padding': '10px'}),
                    html.Div(Y_chart2, style={'width': '50%', 'padding': '10px'})
                ],
                style={'display': 'flex', 'width': '100%'}
            ),

            html.Div(
                className='chart-row',
                children=[
                    html.Div(Y_chart3, style={'width': '50%', 'padding': '10px'}),
                    html.Div(Y_chart4, style={'width': '50%', 'padding': '10px'})
                ],
                style={'display': 'flex', 'width': '100%'}
            )
        ]


    else:
        return None


# Run Server
if __name__ == '__main__':
    app.run(debug=True)

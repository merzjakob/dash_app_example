#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

#load data
filename = 'nama_10_gdp_1_Data.csv'
df = pd.read_csv(filename)
df.head()

app = dash.Dash(__name__)
server = app.server

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

styles = {
    'font-family': 'sans-serif',
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll',
    }
}
#with two DropDown boxes for the different indicators. It will have also a slide for the different years in the data.
available_indicators = df['UNIT'].unique()

app.layout = html.Div([
    #first graph options
    html.Div([
        # indicator dropdown
        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Chain linked volumes, index 2010=100'
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),
        # indicator dropdown
        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Current prices, million euro'
            ),
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),
    #first graph display
    html.Div([
        
        dcc.Graph(id='indicator-graphic'),
        # slider 
        html.Div([
            dcc.Slider(
            id='year--slider',
            min=df['TIME'].min(),
            max=df['TIME'].max(),
            value=df['TIME'].max(),
            step=None,
            marks={str(year): str(year) for year in df['TIME'].unique()}
        )
        ], style= {'margin': '20px'})
        
    ], style={'margin-bottom': '60px', 'padding': '40px'}),

    
    #second graph options
    html.Div([
        html.Div([
            #indicator dropdown
            dcc.Dropdown(
                id='indicator',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Chain linked volumes, index 2010=100'
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),
        # country dropdown
        html.Div([
            dcc.Dropdown(
                id='country',
                options=[{'label': i, 'value': i} for i in df['GEO'].unique()],
                value='European Union - 28 countries'
            ),
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ], style={'padding': '30px'}),
    #second graph display
    html.Div([
        
        dcc.Graph(id='country-graphic'),

    ], style={'margin-bottom': '30px', 'padding': '40px'}), 
])

#first graph callback
@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 year_value):
    dff = df[df['TIME'] == year_value]
    
    return {
        'data': [go.Scatter(
            x=dff[dff['UNIT'] == xaxis_column_name]['Value'],
            y=dff[dff['UNIT'] == yaxis_column_name]['Value'],
            text=dff[dff['UNIT'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
            },
            yaxis={
                'title': yaxis_column_name,
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }


@app.callback(
    #  change country graph
    dash.dependencies.Output('country-graphic', 'figure'),
    # take indicator and country as an input
    [dash.dependencies.Input('indicator', 'value'),
     dash.dependencies.Input('country', 'value')])

def update_graph(indicator_name, country_value):    
    dff = df[df['GEO'] == country_value]
    return {
        'data': [go.Scatter(
            x=list(dff['TIME'].unique()),
            y=dff[dff['UNIT'] == indicator_name]['Value'],
            text=dff[dff['UNIT'] == indicator_name]['GEO'],
            mode='lines',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )     
                ],
        'layout': go.Layout(
            xaxis={
                'title': 'Year',
                'dtick': '1',
                'tickmode': 'linear'
            },
            yaxis={
                'title': indicator_name,
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server()



# coding: utf-8

# In[ ]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash()
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


df = pd.read_csv('nama_10_gdp_1_Data.csv')
df = df[~df.GEO.str.contains('Euro')]
df = df[~df.UNIT.str.contains('Chain')]

#replace country names
df= df.replace({'Germany (until 1990 former territory of the FRG)': 'Germany',
                'Kosovo (under United Nations Security Council Resolution 1244/99)': 'Kosovo',
                'Former Yugoslav Republic of Macedonia, the': 'FYR Maceodonia'
               })

### JOINED VERSION - TWO GRAPHS ###

#create lists for drop-down menus
available_geo = df['GEO'].unique()
available_indicators = df['NA_ITEM'].unique()

app.layout = html.Div([
    #Graph 1 - Scatter Plot
    html.Div([
        
        html.Div([
            'Economic performance of all European countries'
        ],style={'text-align': 'center','font-size': '20px','padding':7}),

        html.Div([
            dcc.Dropdown(
                id='xaxis-column1',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column1',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Wages and salaries'
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),
    
    html.Div([
        dcc.Graph(
            id='indicator-graphic1'
        )
    ],style={'width': '100%', 'display': 'inline-block'}),

    html.Div([
        dcc.Slider(
            id='year--slider',
            min=df['TIME'].min(),
            max=df['TIME'].max(),
            value=df['TIME'].max(),
            step=None,
            marks={str(year): str(year) for year in df['TIME'].unique()}
        )
    ],style={'width': '95%','display': 'inline-block','padding': 10}),

###Graph 2 - Line Chart
    html.Div([
        
        html.Div([
            ''
        ],style={'text-align': 'center','font-size': '20px','height':'30px'}),
        
        html.Div([
            'Economic performance per European country'
        ],style={'text-align': 'center','font-size': '20px','padding':7}),

        html.Div([
            dcc.Dropdown(
                id='xaxis-column2',
                options=[{'label': i, 'value': i} for i in available_geo],
                value='France'
            )
        ],
        style={'width': '45%', 'display': 'inline-block', 'padding': 20}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column2',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Wages and salaries'
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block', 'padding': 20})
    ]),

    dcc.Graph(id='indicator-graphic2'),

])

###Graph 1 - Scatter Plot
@app.callback(
    dash.dependencies.Output('indicator-graphic1', 'figure'),
    [dash.dependencies.Input('xaxis-column1', 'value'),
     dash.dependencies.Input('yaxis-column1', 'value'),
     dash.dependencies.Input('year--slider', 'value')])
def update_graph(xaxis_column_name1, yaxis_column_name1,
                 year_value):
    dff = df[df['TIME'] == year_value]
    
    return {
        'data': [go.Scatter(
            x=dff[(dff['NA_ITEM'] == xaxis_column_name1) & (dff['GEO']==i)]['Value'],
            y=dff[(dff['NA_ITEM'] == yaxis_column_name1) & (dff['GEO']==i)]['Value'],
            text=i,
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }, name = i) for i in available_geo
        ],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name1,
                'type': 'linear'
            },
            yaxis={
                'title': yaxis_column_name1,
                'type': 'linear'
            },
            margin={'l': 60, 'b': 35, 't': 10, 'r': 40},
            hovermode='closest'
        )
    }

###Graph 2 - Line Chart
@app.callback(
    dash.dependencies.Output('indicator-graphic2', 'figure'),
    [dash.dependencies.Input('xaxis-column2', 'value'),
     dash.dependencies.Input('yaxis-column2', 'value')])
def update_graph(xaxis_column_name2, yaxis_column_name2):
    
    dff2=df[df['GEO'] == xaxis_column_name2]
    dff3=dff2[dff2['NA_ITEM'] == yaxis_column_name2]
    
    return {
        'data': [go.Scatter(
            x=dff3['TIME'].unique(),
            y =dff3[dff3['NA_ITEM'] == yaxis_column_name2]['Value'],
            mode='lines'
        )],
        'layout': go.Layout(
            xaxis={
                'title': 'Years',
                'type': 'linear'
            },
            yaxis={
                'title': yaxis_column_name2,
                'type': 'linear'
            },
            margin={'l': 60, 'b': 40, 't': 10, 'r': 40},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server()


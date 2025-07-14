import numpy as np
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import html,dcc
from dash.dependencies import Input, Output


external_stylesheets = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81uXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]
patients = pd.read_csv('IndividualDetails.csv')
total= patients.shape[0]
active=patients[patients['current_status']=='Hospitalized'].shape[0]
recovered=patients[patients['current_status']=='Recovered'].shape[0]
deaths=patients[patients['current_status']=='Deceased'].shape[0]

options=[
    {'label':'All','value':'All'},
    {'label':'Hospitalized','value':'Hospitalized'},
    {'label':'Recovered','value':'Recovered'},
    {'label':'Deceased','value':'Deceased'}
]


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout =html.Div([
    html.H1('Coronovirus pandemic',style={'color':'white','text-align':'center'}),

    html.Div([

        html.Div([
            html.Div([
                html.Div([
                    html.H3("Total cases",style={'color':'white'}),
                    html.H4(total,style={'color':'white'})

                ],className='card-body')
            ],className='card bg-danger')
        ],className='col-md-6'),




        html.Div([
             html.Div([
                html.Div([
                    html.H3("Deaths",style={'color':'white'}),
                    html.H4(deaths,style={'color':'white'})

                ],className='card-body')
            ],className='card bg-success')
        ], className='col-md-3'),


        html.Div([
            html.Div([
                html.Div([
                    html.H3("Active",style={'color':'white'}),
                    html.H4(active,style={'color':'white'})

                ],className='card-body')
            ],className='card bg-info')
        ], className='col-md-3'),


        html.Div([
            html.Div([
                html.Div([
                    html.H3("Recovered",style={'color':'white'}),
                    html.H4(recovered,style={'color':'white'})

                ],className='card-body')
            ],className='card bg-warning')
        ], className='col-md-3')



    ],className='row'),


    html.Div([],className='row'),


    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='picker',options=options,value='All'),
                    dcc.Graph(id='bar')
                ],className='card-body')
            ],className='card')
        ],className='col-md-12')
    ],className='row')
],className='container')
@app.callback(Output('bar','figure'),[Input('picker','value')])
def update_graph(type):
    if type =='All':
        pbar=patients['detected_state'].value_counts().reset_index()
        return {'data':[go.Bar(x=pbar['index'],y=pbar['detected_state'])],'layout':go.layout(title='state total count')}
    else:
        npat=patients[patients['current_status']==type]
        pbar = patients['detected_state'].value_counts().reset_index()
        return {'data': [go.Bar(x=pbar['index'], y=pbar['detected_state'])],
                'layout': go.layout(title='state total count')}

if __name__ == '__main__':
    app.run(debug=True, port=5000)

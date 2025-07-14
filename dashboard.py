import pandas as pd
import plotly.graph_objs as go
import dash
from dash import html,dcc

data = pd.read_csv('gapminder')

app = dash.Dash()
app.layout= html.Div([
    html.Div(children=[
        html.H1('My first dashboard',style={'color':'red','text-align':'center'})
    ],style = {'border':'1px black solid','float':'left','width':'100%','height':'50px'}),
    html.Div(children=[
        dcc.Graph(id='scatter-plot',
                  figure={'data':go.Scatter(x=data['year'],y=data['gdp'],mode='markers')})
             ],style = {'border':'1px black solid','float':'left','width':'49%'}),
    html.Div(style = {'border':'1px black solid','float':'left','width':'49%','height':'350px'})
])


if __name__ =='__main__':
    app.run()



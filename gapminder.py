import numpy as np
import pandas as pd
import dash
from dash import html,dcc,Input,Output,callback,Dash
import plotly.express as px
import plotly.graph_objects as go

from project import continents

df=pd.read_csv('gapminder.csv',encoding='unicode_escape')
options=df['continent'].value_counts().reset_index()

##########Bootstrap is added for layout/style ###########
css=["https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"]
app=dash.Dash(__name__,external_stylesheets=css)

######################################function###############################
def create_table():
    fig = go.Figure(data=[go.Table(
        header=dict(values=df.columns, align='left'),
        cells=dict(values=df.values.T, align='left'))
    ]
    )
    fig.update_layout(paper_bgcolor="#e5ecf6", margin={"t":0, "l":0, "r":0, "b":0}, height=700)
    return fig


def create_graph_pop(continent,year):
    temp_df = df[(df['continent'] == continent) & (df['year'] == year)]
    temp_df = temp_df.sort_values('pop', ascending=False).head(15)
    fig=px.bar(temp_df,x='country',y='pop',color='country')
    return fig

def create_graph_gdp(continent,year):
    temp_df = df[(df['continent'] == continent) & (df['year'] == year)]
    temp_df = temp_df.sort_values('gdpPercap', ascending=False).head(15)
    fig=px.bar(temp_df,x='country',y='gdpPercap',color='country')
    return fig

def create_graph_lifeExp(continent,year):
    temp_df = df[(df['continent'] == continent) & (df['year'] == year)]
    temp_df = temp_df.sort_values('lifeExp', ascending=False).head(15)
    fig=px.bar(temp_df,x='country',y='lifeExp',color='country')
    return fig

#################################WIDGETS#################################
continent=df['continent'].unique()
year=df['year'].unique()

continent_dropdown_pop=dcc.Dropdown(id='cont_pop',options=continent,value='Asia')
year_dropdown_pop=dcc.Dropdown(id='year_pop',options=year,value=1952)

continent_dropdown_gdp=dcc.Dropdown(id='cont_gdp',options=continent,value='Asia')
year_dropdown_gdp=dcc.Dropdown(id='year_gdp',options=year,value=1952)

continent_dropdown_exp=dcc.Dropdown(id='cont_exp',options=continent,value='Asia')
year_dropdown_exp=dcc.Dropdown(id='year_exp',options=year,value=1952)

continent_dropdown_map=dcc.Dropdown(id='cont_map',options=continent,value='Asia')
year_dropdown_map=dcc.Dropdown(id='year_map',options=year,value=1952)



app.layout = html.Div([
    html.H1('Gapminder Dataset Analysis',className='text-center text-white '),
    dcc.Tabs([
        dcc.Tab([html.Br(),dcc.Graph(id='dataset',figure = create_table())],label='Dataset'),

        dcc.Tab([html.Br(),'continents',continent_dropdown_pop,html.Br(),'year',year_dropdown_pop,html.Br(),
                dcc.Graph(id='population')],label='Population'),


        dcc.Tab([html.Br(),'continents',continent_dropdown_gdp, html.Br(),'year',year_dropdown_gdp,html.Br(),
                 dcc.Graph(id='gdp')],label='GDP per capita'),


        dcc.Tab([html.Br(),'continents',continent_dropdown_exp, html.Br(),'year',year_dropdown_exp,html.Br(),
                 dcc.Graph(id='exp')], label='Life Expectancy'),



        dcc.Tab([html.Br(),'continents',continent_dropdown_map, html.Br(),'year',year_dropdown_map,html.Br(),
                 dcc.Graph(id='map')], label='Map'),



    ])
], className="container "),



################################### callback###############################################
@callback(Output('population','fig'),[Input('cont_pop','value'),Input('year_pop','value')])
def update_graph_pop(continent,year):
    return create_graph_pop(continent,year)

@callback(Output('gdp','fig'),[Input('cont_gdp','value'),Input('year_gdp','value')])
def update_graph_gdp(continent,year):
    return create_graph_gdp(continent,year)


@callback(Output('exp','fig'),[Input('cont_exp','value'),Input('year_exp','value')])
def update_graph_pop_lifeExp(continent,year):
    return create_graph_lifeExp(continent,year)





if __name__=='__main__':
    app.run(debug=True)
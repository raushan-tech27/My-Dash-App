import numpy as np
import pandas as pd
import dash
from click import style
from dash import html, dcc, Input, Output, callback,State
import plotly.graph_objects as go
import plotly.express as px

df=pd.read_csv('student_depression_dataset - Copy.csv')
print(df.head())

######################Data cleaning##############################
df.rename(columns={'Have you ever had suicidal thoughts ?':'suicidal thoughts'},inplace=True)

##########################################################################
total_case=df.shape[0]
depression_rate=round(((df['Depression'][df['Depression']==1].sum())/df.shape[0])*100)
total_suicidal=round(((df['suicidal thoughts'][df['suicidal thoughts']=='Yes'].value_counts())/df.shape[0])*100)
avg_work_hours=round(df['Work/Study Hours'].mean(),2)
avg_cgpa=round(df['CGPA'].mean(),2)
gender_option=df['Gender'].unique()
city_option=df['City'].unique()


###Tab1function#####
def create_graph1(Gender='Male',City='Delhi'):
    temp_df = df[(df['Gender'] == Gender) & (df['City'] == City)]
    degree_depression = temp_df.groupby('Degree')['Depression'].mean().reset_index()
    degree_depression['Depression'] *= 100
    fig = px.bar(degree_depression, x=degree_depression['Degree'], y=degree_depression['Depression'],text_auto=True,color='Degree')
    fig.update_layout(height=500, paper_bgcolor="#e5ecf6")
    return fig
#tab2function#####
def create_graph2(Gender='Male',City='Delhi'):
    temp_df = df[(df['Gender'] == Gender) & (df['City'] ==City)]
    sleep_depression = temp_df.groupby('Sleep Duration')['Depression'].mean().reset_index()
    sleep_depression['Depression'] *= 100
    fig=px.bar(sleep_depression,x='Sleep Duration',y='Depression',color='Sleep Duration',
               title='Impact of Sleep Duration on Depression Rate')
    fig.update_layout(height=500, paper_bgcolor="#e5ecf6")
    return fig
#fortab3#######
df_tree = df[df['Depression'] == 1]
df_tree['Gender'] = df_tree['Gender'].astype(str).str.strip().str.title()
df_tree['Degree'] = df_tree['Degree'].astype(str).str.strip()
tree_data = df_tree.groupby(['Degree', 'Gender']).size().reset_index(name='Count')
fig=px.treemap(tree_data,
     path=['Degree', 'Gender'],
     values='Count',
     color='Count',
     color_continuous_scale='Reds',
     title='Treemap of Depression Cases by Degree and Gender')

######function4##########
def create_graph3(Gender='Male',City='Delhi'):
    temp_df = df[(df['Gender'] == Gender) & (df['City'] ==City)]
    grouped = temp_df.groupby('Financial Stress')['suicidal thoughts'].value_counts(normalize=True).unstack().fillna(0)
    suicidal_percent = grouped['Yes'] * 100
    suicidal_percent = suicidal_percent.reset_index().rename(columns={'Yes': 'suicidal_thoughts'})
    fig=px.bar(suicidal_percent,x='Financial Stress',y='suicidal_thoughts',
               color_continuous_scale='Reds',color='Financial Stress',title='Percent of students with suicidal thoughts at each level of financial stress.'
                                                  )
    return fig

css=["https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"]
app=dash.Dash(__name__,external_stylesheets=css)

##########WIDGETS##########
d1=dcc.Dropdown(id='gender1',options=gender_option,value='Male',clearable=False)
d2=dcc.Dropdown(id='city1',options=city_option,value='Delhi',clearable=False)
d3=dcc.Dropdown(id='gender2',options=gender_option,value='Male',clearable=False)
d4=dcc.Dropdown(id='city2',options=city_option,value='Delhi',clearable=False)
d5=dcc.Dropdown(id='gender3',options=gender_option,value='Male',clearable=False)
d6=dcc.Dropdown(id='city3',options=city_option,value='Delhi',clearable=False)

app.layout = html.Div([
    html.Br(),

    html.H1(" 🧠Students Mental Health Dashboard",style={'textAlign':'center','color':'white'}),
    html.Br(),

    html.Div([
######KPI1######
        html.Div([
            html.Div([
                html.Div([html.H3('Total Response'),html.H4(total_case)],className='card-body')
            ],className='card bg-danger text-white')
        ],className='col-md-3'),
#KPI2####
        html.Div([
            html.Div([
                html.Div([html.H3('Avg study Hours/day'), html.H4(avg_work_hours)],className='card-body')
            ],className='card bg-success text-white')
        ],className='col-md-3'),

######KPI3####
       html.Div([
            html.Div([
                html.Div([html.H3('Depression Rate(%)'),html.H4(depression_rate)],className='card-body')
            ],className='card bg-info text-white')
        ],className='col-md-3'),
######KPI4#########
        html.Div([
            html.Div([
                html.Div([html.H3('Suicidal Thoughts(%)'),html.H4(total_suicidal)],className='card-body')
            ],className='card bg-warning text-white')
        ],className='col-md-3')
    ],className='row'),


######after kpis work ###########
    html.Br(),
    html.Div([
        dcc.Tabs([
######tab1#####
            dcc.Tab([html.Br(),'Gender',d1,html.Br(),'City',d2,html.Br(),
                     dcc.Graph(id='bar1')],label='Degree vs Depression Rate'),
####tab2####
            dcc.Tab([html.Br(),'Gender',d3,html.Br(),'City',d4,html.Br(),
                     dcc.Graph(id='bar2')],label='Sleep Duration vs Depression Rate'),
########tab3#########
            dcc.Tab([html.Br(),html.H3('Treemap of Depression Cases by Degree and Gender',
                                       style={'color':'white','textAlign':'center'}),
                     dcc.Graph(id='treemap',figure=fig)],label='Treemap'),


#######tab4########
            dcc.Tab([html.Br(),'Gender',d5,html.Br(),'City',d6,html.Br(),
                     dcc.Graph(id='bar3')],label='Financial stress vs suicidal thoughts'),


        ])
    ],className='row #7f7f7f')


],className='container text-#2ca02c')


@app.callback(Output('bar1','figure'),[Input('gender1','value'),Input('city1','value')])
def update_graph1(Gender,City):
    return create_graph1(Gender,City)

@app.callback(Output('bar2','figure'),[Input('gender2','value'),Input('city2','value')])
def update_graph2(Gender,City):
    return create_graph2(Gender,City)

@app.callback(Output('bar3','figure'),[Input('gender3','value'),Input('city3','value')])
def update_graph3(Gender,City):
    return create_graph3(Gender,City)


if __name__=='__main__':
    app.run(debug=True,port=5000)
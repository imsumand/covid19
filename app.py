import numpy as np
import pandas as pd
import plotly.graph_objects as go
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input,Output
import plotly.express as px
import plotly.offline as pyo
import seaborn as sns
# external CSS stylesheets
external_stylesheets = [
   {
       'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
       'rel': 'stylesheet',
       'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
       'crossorigin': 'anonymous'
   }
]

data=pd.read_csv('covid_19_data.csv')
deaths=pd.read_csv('time_series_covid_19_deaths.csv')
confirmed=pd.read_csv('time_series_covid_19_confirmed.csv')
recovery=pd.read_csv('time_series_covid_19_recovered.csv')
age=pd.read_csv('COVID19_line_list_data.csv')
abc=pd.read_csv('COVID19_open_line_list.csv')
US1=pd.read_csv('time_series_covid_19_confirmed_US.csv')
US2=pd.read_csv('time_series_covid_19_deaths_US.csv')

total_death=deaths['4/5/20'].sum()
total_confirmed=confirmed['4/5/20'].sum()
total_recovery=recovery['4/5/20'].sum()
total_active=total_confirmed-total_death-total_recovery
a=confirmed.set_index('Country/Region')
b = a['4/5/20'].reset_index()
c=recovery.set_index('Country/Region')
d = c['4/5/20'].reset_index()
e=deaths.set_index('Country/Region')
f=e['4/5/20'].reset_index()

hm=confirmed.set_index('Country/Region')
total1=hm['4/5/20'].sort_values(ascending=False).head(10)
total3=total1.reset_index()

ok=recovery.set_index('Country/Region')
total2=ok['4/5/20'].sort_values(ascending=False).head(10)
total4=total2.reset_index()

yes=deaths.set_index('Country/Region')
total6=yes['4/5/20'].sort_values(ascending=False).head(10)
total7=total6.reset_index()

trace1=go.Bar(x=total3['Country/Region'],y=total3['4/5/20'],name='CONFIRMED',marker={'color':'orange'})
trace2=go.Bar(x=total4['Country/Region'],y=total4['4/5/20'],name='RECOVERY',marker={'color':'green'})
data=[trace1,trace2]
layout=go.Layout(title='Recovery/Confirmed of ten most infected countries',barmode='stack')
fig=go.Figure(data=data,layout=layout)

trace3=go.Bar(x=total7['Country/Region'],y=total7['4/5/20'],name='DEATH',marker={'color':'red'})
trace4=go.Bar(x=total4['Country/Region'],y=total4['4/5/20'],name='RECOVERY',marker={'color':'green'})
data1=[trace4,trace3]
layout1=go.Layout(title='Death/Recovery of ten most infected countries',barmode='overlay')
fig1=go.Figure(data=data1,layout=layout1)

a1=age['gender'].dropna().value_counts()
a2=abc['sex'].dropna().value_counts()
a1['female']=a1['female']+a2['female']
a1['male']=a1['male']+a2['male']
a2['male']=a2['male']+a2['Male']
a2['female']=a2['female']+a2['Female']
a10=a1.reset_index()
a11=a10.set_index('gender')
a6=a1.reset_index()
fig3=px.pie(a6,values='gender', names='index',title='infected ratio w.r.t gender(sample population around 2000)')

options=[
   {'label':'confirmed', 'value':'confirmed'},
   {'label':'recovery', 'value':'recovery'},
   {'label':'deaths', 'value':'deaths'}
]

app1 = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app1.layout= html.Div([
    html.H1("COVID-19 pandemic across the globe,till 5th april 2020",style={'color':'#fff','text-align':'center'}),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Total Cases",className='text-light'),
                    html.H4(total_confirmed,className='text-light')
                ],className='card-body')
            ],className='card bg-warning')
        ],className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Active Cases",className='text-light'),
                    html.H4(total_active,className='text-light')
                ],className='card-body')
            ],className='card bg-info')
        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Deaths",className='text-light'),
                    html.H4(total_death,className='text-light')
                ],className='card-body')
            ],className='card bg-danger')
        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Recovered",className='text-light'),
                    html.H4(total_recovery,className='text-light')
                ],className='card-body')
            ],className='card bg-success')
        ], className='col-md-3')
    ],className='row'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(figure=fig)
                ],className='card-body')
            ],className='card')
        ],className='col-md-6'),
        html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(figure=fig1)
                ],className='card-body')
            ],className='card')
        ],className='col-md-6'),
    ],className='row'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(figure=fig3)
                ], className='card-body')
            ], className='card')
        ], className='col-md-12'),
    ],className='row'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='picker',options=options, value='confirmed'),
                    dcc.Graph(id='bar')
                ], className='card-body')
            ],className='card')
        ],className='col-md-12')
    ],className='row')
],className='container')


@app1.callback(Output('bar', 'figure'), [Input('picker', 'value')])
def update_graph(type):
    if type=="confirmed":
        return {'data': [go.Bar(x=b['Country/Region'], y=b['4/5/20'])],
                'layout': go.Layout(title='Counts by country')}
    elif type=="recovery":
        return {'data': [go.Bar(x=d['Country/Region'], y=d['4/5/20'])],
                'layout': go.Layout(title='Counts by country')}
    else:
        return {'data': [go.Bar(x=f['Country/Region'], y=f['4/5/20'])],
                'layout': go.Layout(title='Counts by country')}
if __name__=="__main__":
   app1.run_server(debug=True,port=5000)
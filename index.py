import dash
from dash import html
from dash import dcc
from dash.dcc.Graph import Graph
from dash.dependencies import Input, Output
from dash.html.Div import Div
from dash.html.H1 import H1
from dash.html.Title import Title
from numpy import number
import plotly.graph_objects as go
import pandas as pd

url_confirmed = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
url_deaths = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
url_recovered = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'

confirmed = pd.read_csv(url_confirmed)
deaths = pd.read_csv(url_deaths)
recovered = pd.read_csv(url_recovered)

# unpivot data
date1 = confirmed.columns[4:]
total_confirmed = confirmed.melt(id_vars=['Province/State','Country/Region','Lat','Long'],
    value_vars=date1,
    var_name='date',
    value_name='confirmed')

date2 = deaths.columns[4:]
total_deaths = deaths.melt(id_vars=['Province/State','Country/Region','Lat','Long'],
    value_vars=date2,
    var_name='date',
    value_name='deaths')

date3 = recovered.columns[4:]
total_recovered = recovered.melt(id_vars=['Province/State','Country/Region','Lat','Long'],
    value_vars=date3,
    var_name='date',
    value_name='recovered')

# merging data frames
covid_data = total_confirmed.merge(right = total_deaths,
    how='left',
    on=['Province/State','Country/Region','Lat','Long','date'],
    )
covid_data = covid_data.merge(right = total_recovered,
    how='left',
    on=['Province/State','Country/Region','Lat','Long','date'],
    )

# converting date format from string on date column
covid_data['date'] = pd.to_datetime(covid_data['date'])

# checking sum of missing values
covid_data.isna().sum()

# replacing with zero
covid_data['recovered'] = covid_data['recovered'].fillna(0)

# adding new column
covid_data['active'] = covid_data['confirmed'] - covid_data['deaths'] - covid_data['recovered']


covid_data_1 = covid_data.groupby(['date'])[['confirmed','deaths','recovered','active']].sum().reset_index()


# creating layout of the dash app
app = dash.Dash(__name__, )

app.layout = html.Div([

    #header
    html.Div([

        # logo
        html.Div([
            html.Img(src=app.get_asset_url('covidlogo.png'),
            id='covid-image',
            style={'height':'60px',
                    'withd':'auto',
                    'margin-bottom':'25px'})
        ], className='one-third column'),

        # title
        html.Div([
            html.Div([
                html.H3('Covid - 19', style={'margin-bottom':'0px', 'color':'white'}),
                html.H5('Tracking Covid Dashboard', style={'margin-bottom':'0px', 'color':'white'})
            ])
        ],className='one-half column',id='title'),

        # latest day updated
        html.Div([
            html.H6('Last Update: '+ str(covid_data['date'].iloc[-1].strftime('%B %d,%Y')) + ' 00:01 (UTC)',
                    style={'color':'orange'})
        ], className='one-third column', id='title1')   

    ], id='header', className='row flex-display',style={'margin-bottom':'25px'}),

    #main body
    html.Div([

        html.Div([
            html.H6(children='Global Cases',style={'textAlign':'center',
                                                    'color':'white'}),
            html.P(f"{covid_data_1['confirmed'].iloc[-1]:,.0f}",style={'textAlign':'center',
                                                    'color':'orange',
                                                    'fontSize':40}),
            html.P('new cases: '+ f"{covid_data_1['active'].iloc[-1] - covid_data_1['active'].iloc[-2]:,.0f}"
                    + '(' + str(round(((covid_data_1['active'].iloc[-1] - covid_data_1['active'].iloc[-2]) / 
                                        covid_data_1['confirmed'].iloc[-1]) * 100,2)) + '%)',
                                                style={
                                                    'textAlign':'center',
                                                    'color':'orange',
                                                    'fontSize': 15,
                                                    'margin-top':'-18px'})

        ], className='card_container three columns'),

        html.Div([
            html.H6(children='Global Deaths',style={'textAlign':'center',
                                                    'color':'white'}),
            html.P(f"{covid_data_1['deaths'].iloc[-1]:,.0f}",style={'textAlign':'center',
                                                    'color':'#dd1e35',
                                                    'fontSize':40}),
            html.P('new deaths: '+ f"{covid_data_1['deaths'].iloc[-1] - covid_data_1['deaths'].iloc[-2]:,.0f}"
                    + '(' + str(round(((covid_data_1['deaths'].iloc[-1] - covid_data_1['deaths'].iloc[-2]) / 
                                        covid_data_1['deaths'].iloc[-1]) * 100,2)) + '%)',
                                                style={
                                                    'textAlign':'center',
                                                    'color':'#dd1e35',
                                                    'fontSize': 15,
                                                    'margin-top':'-18px'}),

        ], className='card_container three columns'),

        html.Div([
            html.H6(children='Global Recovered',style={'textAlign':'center',
                                                    'color':'white'}),
            html.P(f"{covid_data_1['recovered'].iloc[-51]:,.0f}",style={'textAlign':'center',
                                                    'color':'green',
                                                    'fontSize':40}),
            html.P('new recovered: '+ f"{covid_data_1['recovered'].iloc[-1] - covid_data_1['recovered'].iloc[-2]:,.0f}"
                    + '(' + str(round(((covid_data_1['recovered'].iloc[-1] - covid_data_1['recovered'].iloc[-2]) / 
                                        covid_data_1['recovered'].iloc[-1]) * 100,2)) + '%)',
                                                style={
                                                    'textAlign':'center',
                                                    'color':'green',
                                                    'fontSize': 15,
                                                    'margin-top':'-18px'}),

        ], className='card_container three columns'),

        html.Div([
            html.H6(children='Global Active',style={'textAlign':'center',
                                                    'color':'white'}),
            html.P(f"{covid_data_1['active'].iloc[-1]:,.0f}",style={'textAlign':'center',
                                                    'color':'#e55467',
                                                    'fontSize':40}),
            html.P('new active: '+ f"{covid_data_1['active'].iloc[-1] - covid_data_1['active'].iloc[-2]:,.0f}"
                    + '(' + str(round(((covid_data_1['active'].iloc[-1] - covid_data_1['active'].iloc[-2]) / 
                                        covid_data_1['active'].iloc[-1]) * 100,2)) + '%)',
                                                style={
                                                    'textAlign':'center',
                                                    'color':'#e55467',
                                                    'fontSize': 15,
                                                    'margin-top':'-18px'}),

        ], className='card_container three columns')

    ], className='row flex-display'),


    html.Div([
        html.Div([
            html.P('Select Country:', className='fix_label', style={'color':'white'}),
            dcc.Dropdown(id='w_countries',
                        multi=False,
                        searchable= True,
                        value='Canada',
                        placeholder='Select Countries',
                        options=[{'label': c, 'value': c}
                                    for c in (covid_data['Country/Region'].unique())], className='dcc_compon'),

            html.P('New Cases: ' + ' ' + str(covid_data['date'].iloc[-1].strftime('%B %d,%Y')),
                    className='fix_label', style={'text-align':'center', 'color':'white'}),

            dcc.Graph(id='confirmed', config={'displayModeBar':False}, className='dcc_compon',
                        style={'margin-top':'20px'}),

            dcc.Graph(id='deaths', config={'displayModeBar':False}, className='dcc_compon',
                        style={'margin-top':'20px'}),

            dcc.Graph(id='recovered', config={'displayModeBar':False}, className='dcc_compon',
                        style={'margin-top':'20px'}),

            dcc.Graph(id='active', config={'displayModeBar':False}, className='dcc_compon',
                        style={'margin-top':'20px'}),
            
            

        ], className='create_container three columns'),

        html.Div([
            dcc.Graph(id='pie_chart', config={'displayModeBar':'hover'}),

        ], className='create_container four column'),

        html.Div([
            dcc.Graph(id='line_chart', config={'displayModeBar':'hover'}),

        ], className='create_container five column')

    ],className='row flex-display')

], id = 'mainContainer', style={'display':'flex', 'flex-direction':'column'})

@app.callback(Output('confirmed','figure'),
                    [Input('w_countries','value')])

def update_confirmed(w_countries):
    covid_data_2 = covid_data.groupby(['date','Country/Region'])[['confirmed','deaths','recovered','active']].sum().reset_index()
    value_confirmed = covid_data_2[covid_data_2['Country/Region']==w_countries]['confirmed'].iloc[-1] - covid_data_2[covid_data_2['Country/Region']==w_countries]['confirmed'].iloc[-2]
    delta_confirmed = covid_data_2[covid_data_2['Country/Region']==w_countries]['confirmed'].iloc[-2] - covid_data_2[covid_data_2['Country/Region']==w_countries]['confirmed'].iloc[-3]

    return{
        'data':[go.Indicator(
            mode='number+delta',
            value=value_confirmed,
            delta= {'reference':delta_confirmed,
                    'position':'right',
                    'valueformat':',g',
                    'relative':False,
                    'font':{'size':15}},
            number={'valueformat':',',
                    'font':{'size':20}},
            domain={'y':[0,1],'x':[0,1]}
        )],

        'layout': go.Layout(
            title={'text':'New Confirmed',
                    'y':1,
                    'x':0.5,
                    'xanchor':'center',
                    'yanchor':'top'},
            font = dict(color='orange'),
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            height = 50,
        )
    }


@app.callback(Output('deaths','figure'),
                    [Input('w_countries','value')])

def update_confirmed(w_countries):
    covid_data_2 = covid_data.groupby(['date','Country/Region'])[['confirmed','deaths','recovered','active']].sum().reset_index()
    value_deaths = covid_data_2[covid_data_2['Country/Region']==w_countries]['deaths'].iloc[-1] - covid_data_2[covid_data_2['Country/Region']==w_countries]['deaths'].iloc[-2]
    delta_deaths = covid_data_2[covid_data_2['Country/Region']==w_countries]['deaths'].iloc[-2] - covid_data_2[covid_data_2['Country/Region']==w_countries]['deaths'].iloc[-3]

    return{
        'data':[go.Indicator(
            mode='number+delta',
            value=value_deaths,
            delta= {'reference':delta_deaths,
                    'position':'right',
                    'valueformat':',g',
                    'relative':False,
                    'font':{'size':15}},
            number={'valueformat':',',
                    'font':{'size':20}},
            domain={'y':[0,1],'x':[0,1]}
        )],

        'layout': go.Layout(
            title={'text':'New Deaths',
                    'y':1,
                    'x':0.5,
                    'xanchor':'center',
                    'yanchor':'top'},
            font = dict(color='#dd1e35'),
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            height = 50,
        )
    }

@app.callback(Output('recovered','figure'),
                    [Input('w_countries','value')])

def update_confirmed(w_countries):
    covid_data_2 = covid_data.groupby(['date','Country/Region'])[['confirmed','deaths','recovered','active']].sum().reset_index()
    value_recovered = covid_data_2[covid_data_2['Country/Region']==w_countries]['recovered'].iloc[-1] - covid_data_2[covid_data_2['Country/Region']==w_countries]['recovered'].iloc[-2]
    delta_recovered = covid_data_2[covid_data_2['Country/Region']==w_countries]['recovered'].iloc[-2] - covid_data_2[covid_data_2['Country/Region']==w_countries]['recovered'].iloc[-3]

    return{
        'data':[go.Indicator(
            mode='number+delta',
            value=value_recovered,
            delta= {'reference':delta_recovered,
                    'position':'right',
                    'valueformat':',g',
                    'relative':False,
                    'font':{'size':15}},
            number={'valueformat':',',
                    'font':{'size':20}},
            domain={'y':[0,1],'x':[0,1]}
        )],

        'layout': go.Layout(
            title={'text':'New Recovered',
                    'y':1,
                    'x':0.5,
                    'xanchor':'center',
                    'yanchor':'top'},
            font = dict(color='green'),
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            height = 50,
        )
    }

@app.callback(Output('active','figure'),
                    [Input('w_countries','value')])

def update_confirmed(w_countries):
    covid_data_2 = covid_data.groupby(['date','Country/Region'])[['confirmed','deaths','recovered','active']].sum().reset_index()
    value_active = covid_data_2[covid_data_2['Country/Region']==w_countries]['active'].iloc[-1] - covid_data_2[covid_data_2['Country/Region']==w_countries]['active'].iloc[-2]
    delta_active = covid_data_2[covid_data_2['Country/Region']==w_countries]['active'].iloc[-2] - covid_data_2[covid_data_2['Country/Region']==w_countries]['active'].iloc[-3]

    return{
        'data':[go.Indicator(
            mode='number+delta',
            value=value_active,
            delta= {'reference':delta_active,
                    'position':'right',
                    'valueformat':',g',
                    'relative':False,
                    'font':{'size':15}},
            number={'valueformat':',',
                    'font':{'size':20}},
            domain={'y':[0,1],'x':[0,1]}
        )],

        'layout': go.Layout(
            title={'text':'New Active',
                    'y':0.9,
                    'x':0.5,
                    'xanchor':'center',
                    'yanchor':'top'},
            font = dict(color='#e55467'),
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            height = 50,
        )
    }


@app.callback(Output('pie_chart','figure'),
                    [Input('w_countries','value')])

def update_graph(w_countries):
    covid_data_2 = covid_data.groupby(['date','Country/Region'])[['confirmed','deaths','recovered','active']].sum().reset_index()
    confirmed_value = covid_data_2[covid_data_2['Country/Region']==w_countries]['confirmed'].iloc[-1] 
    deaths_value = covid_data_2[covid_data_2['Country/Region']==w_countries]['deaths'].iloc[-1] 
    recovered_value = covid_data_2[covid_data_2['Country/Region']==w_countries]['recovered'].iloc[-1] 
    active_value = covid_data_2[covid_data_2['Country/Region']==w_countries]['active'].iloc[-1] 

    colors = ['orange','red','green','#e55467']

    return{
        'data':[go.Pie(
            labels=['Confirmed','Deaths','Recovered','Active'],
            values = [confirmed_value,deaths_value,recovered_value,active_value],
            marker = dict(colors=colors),
            hoverinfo = 'label+value+percent',
            textinfo = 'label+value',
            hole=.7,
            rotation=90,
            
        )],

        'layout': go.Layout(
            title={'text':'Total Cases: '+ (w_countries),
                    'y':0.9,
                    'x':0.5,
                    'xanchor':'center',
                    'yanchor':'top'},
            titlefont={'color':'white',
                        'size':20},
            font=dict(family='sans-serif',
                        color='white',
                        size=12),
            hovermode='closest',
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            legend={'orientation':'h',
                    'bgcolor':'#1f2c56',
                    'xanchor':'center','x':0.5,'y':-0.7}
            
        )
    }

@app.callback(Output('line_chart','figure'),
                    [Input('w_countries','value')])

def update_graph(w_countries):
    covid_data_2 = covid_data.groupby(['date','Country/Region'])[['confirmed','deaths','recovered','active']].sum().reset_index()
    covid_data_3 = covid_data_2[covid_data_2['Country/Region']==w_countries][['Country/Region','date','confirmed']].reset_index()
    covid_data_3['dailyconfirmed']=covid_data_3['confirmed'] = covid_data_3['confirmed'].shift(1)
    covid_data_3['rollingAve'] = covid_data_3['dailyconfirmed'].rolling(window=7).mean()

    

    return{
        'data':[go.Bar(
            x= covid_data_3['date'].tail(30),
            y= covid_data_3['dailyconfirmed'].tail(30),
            name='Daily Confirmed Cases',
            marker=dict(color='orange'),
            hoverinfo = 'text',
            hovertext=
            '<b>Date</b>: ' + covid_data_3['date'].tail(30).astype(str) + '<br>' +
            '<b>Confirmed Cases</b>: ' + [f'{x:,.0f}' for x in covid_data_3['dailyconfirmed'].tail(30)] + '<br>' +
            '<b>Country</b>: ' + covid_data_3['Country/Region'].tail(30).astype(str) + '<br>',
            
        ),
            go.Scatter(
            x= covid_data_3['date'].tail(30),
            y= covid_data_3['rollingAve'].tail(30),
            name='Rolling Average of the last 7 days - daily confirmed cases',
            mode='lines',
            line=dict(width=3,color='#FF00FF'),
            hoverinfo = 'text',
            hovertext=
            '<b>Date</b>: ' + covid_data_3['date'].tail(30).astype(str) + '<br>' +
            '<b>Confirmed Cases</b>: ' + [f'{x:,.0f}' for x in covid_data_3['rollingAve'].tail(30)] + '<br>' 
            
        )
        ],

        'layout': go.Layout(
            title={'text':'Last 30 days Daily Confirmed Cases: '+ (w_countries),
                    'y':0.9,
                    'x':0.5,
                    'xanchor':'center',
                    'yanchor':'top'},
            titlefont={'color':'white',
                        'size':20},
            font=dict(family='sans-serif',
                        color='white',
                        size=12),
            hovermode='closest',
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            legend={'orientation':'h',
                    'bgcolor':'#1f2c56',
                    'xanchor':'center','x':0.5,'y':-0.7},
            margin=dict(r=0),
            xaxis=dict(title='<b>Date</b>',
                        color='white',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='white',
                        linewidth=1,
                        ticks='outside',
                        tickfont=dict(
                            family='Aerial',
                            color='white',
                            size=12
                        )),
            yaxis=dict(title='<b>Daily Confirmed Cases: </b>',
                        color='white',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='white',
                        linewidth=1,
                        ticks='outside',
                        tickfont=dict(
                            family='Aerial',
                            color='white',
                            size=12
                        ))
            
        )
    }




if __name__ == '__main__':
    app.run_server(debug=True)
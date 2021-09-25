import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from dash.html.Div import Div
from dash.html.H1 import H1
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
            html.P('new recovered: '+ f"{covid_data_1['recovered'].iloc[-51] - covid_data_1['recovered'].iloc[-52]:,.0f}"
                    + '(' + str(round(((covid_data_1['recovered'].iloc[-51] - covid_data_1['recovered'].iloc[-52]) / 
                                        covid_data_1['recovered'].iloc[-51]) * 100,2)) + '%)',
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

    ], className='row flex-display')

], id = 'mainContainer', style={'display':'flex', 'flex-direction':'column'})

if __name__ == '__main__':
    app.run_server(debug=True)
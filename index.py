import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
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
    value_vars=date2,
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

# creating layout of the dash app
app = dash.Dash(__name__, )

app.layout = html.Div([
    
])

if __name__ == '__main__':
    app.run_server(debug=True)
#!/usr/bin/env python
import numpy as np
import pandas as pd
# disable chained assignments
pd.options.mode.chained_assignment = None
import os
import requests
from zipfile import ZipFile
from io import BytesIO
import dotenv
import json
from datetime import datetime, timedelta

import plotly.express as px
from bokeh.plotting import figure, output_file, show, save, ColumnDataSource
from bokeh.models import Range1d
from bokeh.models.tools import HoverTool
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.transform import factor_cmap
from bokeh.palettes import Blues8
from bokeh.embed import components

dotenv_config = {
    **os.environ,  # override loaded values with environment variables
}
    #**dotenv.dotenv_values(".env"),  # load shared development variables
print(dotenv_config)
key=dotenv_config['ALPHA_VANTAGE_API_KEY']

ticker = 'IBM'
#ticker = 'SHOP.TRT'
#options='adjusted=true&'
options=''
#function='TIME_SERIES_INTRADAY'
#function='TIME_SERIES_MONTHLY_ADJUSTED'
function='TIME_SERIES_DAILY'
sample_date='2021-12-24'

def get_data():
    #url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&apikey={}'.format(ticker, key)
    url = 'https://www.alphavantage.co/query?function={}&symbol={}&interval=5min&{}apikey={}'.format(function,ticker,options,key)
    req = requests.get(url)
    #print(req.json())
    df=pd.read_json(req.content)
    return df

def symbol_search(keyword): #search for available ticker symbols
    url = 'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={}&apikey={}'.format(keyword,key)
    req = requests.get(url)
    #print(req.json())
    df=pd.read_json(req.content)
    return df

df = get_data()
#df.drop(df.index[range(0,4)],inplace=True) #delete header lines
df.drop(df.index[range(0,5)],inplace=True) #delete header lines
#print(df)
print(df.index) #to see available dates (one per month)
#print('------')
#print(df.loc[sample_date][1]) #to see the types of values for each date
#print(df.loc[sample_date][1]['4. close']) #closing price for one date
#print('------')
#print(df['Time Series (Daily)'])
#print('------')
df["closing"]=df['Time Series (Daily)'].map(
                    lambda x: str(x['4. close'])
                    ) #the values need to be string not float otherwise bokeh mad about y_range
df['date']=df.index.map(
                    lambda x: datetime.strptime(x,'%Y-%m-%d')
                    ) #need to convert the index which contains the date as a string to a usable object to plot. Creating a duplicate column is not maybe the most optimized but whatever

#df.reset_index(inplace=True)

#print(df['closing'])

print('------')
source = ColumnDataSource(df)
#print(source.data['closing'])
#print(source.data['date'])
#print(source.data)
#print('------')

output_file('index.html')

p = figure(
    plot_width=800,
    plot_height=600,
    title='Daily Non-Adjusted Closing Price',
    x_axis_label='Date',
    x_axis_type="datetime",
    y_axis_label='Closing Price',
    tools="pan,box_select,zoom_in,zoom_out,save,reset",
)
    #y_range=source.data['closing'].tolist(),
    #x_range=source.data['index'].tolist(),
    #y_range=Range1d(1700,2000),
    #x_range=Range1d(0,100),

p.xaxis.formatter=DatetimeTickFormatter(months='%b %Y')

p.toolbar.logo = None
p.toolbar_location = None
p.toolbar.active_drag = None
p.toolbar.active_scroll = None
p.toolbar.active_tap = None

p.border_fill_color = 'black'
p.background_fill_color = 'black'
p.outline_line_color = 'lightgrey'
p.grid.grid_line_color = 'slategrey'
p.border_fill_color = 'black'

p.title.text_color = 'white'
p.title.align= 'center'
p.title.text_font_size = '20px'
p.title.text_font_style = "bold"

p.xaxis.major_label_text_color = 'white'
p.yaxis.major_label_text_color = 'white'
p.xaxis.axis_label_text_color = 'white'
p.yaxis.axis_label_text_color = 'white'
p.xaxis.axis_line_color = "white"
p.yaxis.axis_line_color = "white"
p.xaxis.axis_label_text_font_size = '16px'
p.yaxis.axis_label_text_font_size = '16px'


p.line(
        x=source.data['date'],
        y=source.data['closing'],
        color='cyan',
        line_width=2,
        legend_label=ticker
        )
        #x=source.data['level_0'],


p.legend.location = 'top_left'
p.legend.title = 'Ticker'
p.legend.title_text_font_style = "bold"
p.legend.title_text_font_size = "20px"
p.legend.title_text_color = 'white'
p.legend.label_text_color = 'white'
p.legend.border_line_width = 3
p.legend.border_line_color = "white"
p.legend.border_line_alpha = 0.1
p.legend.background_fill_color = "white"
p.legend.background_fill_alpha = 0.05

save(p)
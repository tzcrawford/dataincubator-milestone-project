#!/usr/bin/env python
import numpy as np
import pandas as pd
# disable chained assignments
pd.options.mode.chained_assignment = None
import geopandas as gpd
import streamlit as st
import plotly.express as px
from zipfile import ZipFile
import requests
from io import BytesIO
import json

key = 'XXX'
ticker = 'AAPL'

@st.cache
def get_data():
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&apikey={}'.format(ticker, key)
    req = requests.get(url)
    print(response.json())
    #content=ZipFile(BytesIO(req.content))
    #df=pd.read_csv(content.open("geochem.csv"))
    #df=pd.read_csv(content.open("geochem.csv"))[['LABNO','CATEGORY','DATASET','TYPEDESC','ICP40_JOB','AS_ICP40','AS_AA','LATITUDE','LONGITUDE']]
    #df=gpd.read_file(content.open('ngs.shp'))
    df=gpd.read_file(BytesIO(req.content))
    #,rows=100)[['LABNO','CATEGORY','DATASET','TYPEDESC','COUNT','ICP40_JOB','AS_ICP40','AS_AA','geometry']]
    return df

df = get_data()

st.title("Streamlit 101: An in-depth introduction")
st.markdown("This is a Subtitle!")

#st.code("""
#def square(x):
#    return x**2
#""", language="python")

st.markdown("**Columns are:**\n"+str(df.columns.values))
#df=df[['REC_NO','LABNO','COLL_DATE','CATEGORY','DATASET','TYPEDESC','ICP40_JOB','AS_ICP40','AS_AA','LATITUDE','LONGITUDE']]
df=df[['LABNO','CATEGORY','DATASET','TYPEDESC','ICP40_JOB','AS_ICP40','AS_AA','geometry']]
#df.rename(columns={'LATITUDE': 'lat', 'LONGITUDE': 'lon'}, inplace=True)
#df.set_index('REC_NO')
df.set_index('geometry')
st.markdown(df.shape[0])
df.drop(range(1000,len(df)),inplace=True)
st.markdown(df.shape[0])

#st.header("Head of Raw Data")
#st.dataframe(df.head()) #err for some reason

def web_mercator(df, lon="lon", lat="lat"):
    #Convert decimal lon/lat to Web Mercator format
    k=6378137
    df["x"]=df[lon]*k*np.pi/180.0
    df["y"]=np.log( np.tan( (90 + df[lat]) * np.pi / 360 ) ) * k 
    return df
df['lon']=df['geometry'].map(
        lambda x: float(str(x).strip("POINT (").replace(" ",",").strip(")").split(",")[0])
        )   
df['lat']=df['geometry'].map(
        lambda x: float(str(x).strip("POINT (").replace(" ",",").strip(")").split(",")[1])
        )
df=web_mercator(df)
df['AS_ICP40'].replace('',np.nan, inplace=True)
df['AS_ICP40'].replace(' ',np.nan, inplace=True)
df['lat'].replace('',np.nan, inplace=True)
df['lat'].replace(' ',np.nan, inplace=True)
#df.dropna(subset=['AS_ICP40'], inplace=True, how='any')
df.dropna(inplace=True)

USA = x_range,y_range = ((-13884029,-7453304), (2698291,6455972))
map_bkg_url="http://a.basemaps.cartocdn.com/rastertiles/voyager/{Z}/{X}/{Y}.png"
map_bkpg_attribution="Tiles by Carto, under CC BY 3.0"


st.map(df)

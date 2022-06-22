# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 12:32:15 2022

@author: Bruker
"""
import numpy as np
import pandas as pd
import streamlit as st
import nasdaqdatalink as ndl
import yfinance as yf
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

#%% Oprett datoer for start og slutt på plott/data
dagens_dato = datetime.utcnow().date()
delta_2y = timedelta(days=730)#1095)
start_dato = dagens_dato-delta_2y

#%% Hent data fra yfinance og nasdagdatalink
bm_data = ndl.get("ECONOMIST/BIGMAC_USA")
bm_data_ = bm_data.loc[start_dato:]
big_mac_price = bm_data_["dollar_price"]

cpi_data = ndl.get("RATEINF/CPI_USA")
cpi_data_ = cpi_data.loc [start_dato:]

vix_data = yf.download("^VIX", start=start_dato, end=dagens_dato)
vix_data_ = vix_data["Open"]

sp500_data = yf.download("^GSPC", start=start_dato, end=dagens_dato)
sp500_data_ = sp500_data["Open"]

interest_data = yf.download("^TNX", start=start_dato, end=dagens_dato)
interest_data_ = interest_data["Open"]

tech_stoc_data = yf.download("^NDXT", start=start_dato, end=dagens_dato)
tech_stoc_data_ = tech_stoc_data["Open"]

#%%Plott data i linjediagrammer 
fig = plt.figure()
gs = fig.add_gridspec(4, hspace=0)
axs = gs.subplots(sharex=True)

p0 = axs[0].plot(tech_stoc_data_.index, tech_stoc_data_.values, 'tab:green')
axs[0].set_ylabel('NASDAQ_Tech')
p1 = axs[1].plot(interest_data_.index, interest_data_.values,'tab:blue')
axs[1].set_ylabel('Yield')
p2 = axs[2].plot(cpi_data_.index, cpi_data_.values,'tab:orange')
axs[2].set_ylabel('CPI')
p3 = axs[3].plot(big_mac_price.index, big_mac_price.values,'tab:red')
axs[3].set_ylabel('BigMac')

plt.xticks(rotation=45)

#st.pyplot(fig)
#%% Plott mer data i nytt diagram
fig_ = plt.figure()
gs_ = fig_.add_gridspec(2, hspace=0)
axs = gs_.subplots(sharex=True)

p4 = axs[0].plot(sp500_data_.index, sp500_data_.values, 'tab:green')
axs[0].set_ylabel('S&P 500')
p5 = axs[1].plot(vix_data_.index, vix_data_.values,'tab:blue')
axs[1].set_ylabel('VIX')

plt.xticks(rotation=45)
#%%Pressenter data på nettside
cpi_delta = cpi_data_["Value"].iloc[-1]/cpi_data_["Value"].iloc[0]
cpi_delta = (cpi_delta-1)*100
cpi_delta= round(cpi_delta,1)
st.write("I følge Consumer Price Index har prisene på varer økt med:", cpi_delta,"% de siste 2 årene" )


st.write( "Plottet under viser sammenhengen VIX-en og S&P500 de siste 2 årene")
st.pyplot(fig_)

st.write( "Plottet under viser sammenhengen mellom inflasjon, renter og teknologi aksjer de siste 2 årene")
st.pyplot(fig)




import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

# Sample data
df = yf.Ticker('GOOGL').history(period='1y')

# 1. Native Streamlit Line Chart
st.line_chart(df['Close'])

# 2. Interactive Plotly Chart
import plotly.express as px
fig = px.line(df, x=df.index, y='Close', color='Close', title='GOOGL Closing Prices')
st.plotly_chart(fig)

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import pathlib

my_ticker = pd.read_csv('my_ticker.txt', header=None, skipinitialspace=True).iloc[0, :].tolist()

print(my_ticker)
# Sample data

for x in my_ticker:
    if not pathlib.Path(f'./pages/{x}.py').exists():
        pathlib.Path(f'./pages/{x}.py').touch()
        file_path = pathlib.Path(f'./pages/{x}.py')
        python_code = f"""
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np


def get_data(ticker):
    data = yf.Ticker(ticker)
    hist = data.history(period="1y")
    return hist

st.title("Stock Price Visualization")

ticker = st.text_input("Enter a stock ticker symbol:", "{x}")
if ticker:
    data = get_data(ticker)
    st.line_chart(data['Close'])

            """
        file_path.write_text(python_code)

df_ticker = pd.read_csv('all_tickers.txt', sep='\t', header=0)

print(df_ticker)

df = yf.Ticker('GOOGL').history(period='1y')

# 1. Native Streamlit Line Chart
st.line_chart(df['Close'])

# 2. Interactive Plotly Chart
import plotly.express as px
fig = px.line(df, x=df.index, y='Close', color='Close', title='GOOGL Closing Prices')
st.plotly_chart(fig)

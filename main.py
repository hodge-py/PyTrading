import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import pathlib
from streamlit_searchbox import st_searchbox
import csv

watchlistPath = pathlib.Path('watchlist.csv')

if not watchlistPath.exists():
    with open('watchlist.csv', 'w') as f:
        f.write("")
else:
    pass

df_ticker = pd.read_csv('all_tickers.txt', sep='\t', header=0)

#print(df_ticker)

tickerAsList = df_ticker['Companies'].tolist()

def search_tickers(search_term: str):
    if not search_term:
        return tickerAsList[:5] 
    
    # Filter the list based on what the user typed (case-insensitive)
    return [str(t) for t in tickerAsList if search_term.upper() in str(t).upper()]

#print(tickerAsList)

col1, col2, col3 = st.columns([5,1,2])

with col1:
    selected_ticker = st_searchbox(
    search_function=search_tickers,
    placeholder="Search for a stock ticker... Ex. AAPL MSFT GOOGL",
    key="ticker_searchbox",
)

with col2:
    search_clicked = st.button("Search")

with col3:
    search_add = st.button("Add to Watchlist")

if search_clicked and selected_ticker:
    st.subheader(f"Results for {selected_ticker}")
    
    # This is where you'd put your yfinance / Plotly code
    st.info(f"Fetching live data for {selected_ticker}...")

    
    df = yf.Ticker(selected_ticker).history(period='1y')

    # 1. Native Streamlit Line Chart
    st.line_chart(df['Close'])

    # 2. Interactive Plotly Chart
    import plotly.express as px
    fig = px.line(df, x=df.index, y='Close', color='Close', title='GOOGL Closing Prices')
    st.plotly_chart(fig)

elif search_clicked and not selected_ticker:
    st.warning("Please select a ticker from the list first!")

if search_add and selected_ticker:
    selected_ticker = selected_ticker.upper()
    flag = False

    with open('watchlist.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            # Check if the word is in the current row (which is a list of strings)
            if selected_ticker in row:
                flag = True
                break

    if not flag:
        with open('watchlist.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([selected_ticker])
        st.success(f"{selected_ticker} added to watchlist!")
    else:
        st.warning(f"{selected_ticker} already exists in watchlist!")

    
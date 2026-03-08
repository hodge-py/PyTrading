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

    tick = yf.Ticker(selected_ticker)
    
    # This is where you'd put your yfinance / Plotly code
    st.info(f"Fetching live data for {selected_ticker}... {tick.info['longName']}...")    
    
    df = tick.history(period='1y').dropna()  # Drop rows with NaN values to avoid issues with plotting
    
    # 1. Native Streamlit Line Chart
    st.line_chart(df['Close'])

    import plotly.graph_objects as go
    fig = go.Figure(data=[go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])
    
    dt_all = pd.date_range(start=df.index.min(), end=df.index.max())
    dt_obs = [d.strftime("%Y-%m-%d") for d in df.index]
    # These are your holidays and weekends
    dt_breaks = [d for d in dt_all.strftime("%Y-%m-%d").tolist() if not d in dt_obs]

    fig.update_xaxes(
        rangebreaks=[
            dict(bounds=["sat", "mon"]), # Hides all weekends
            dict(values=dt_breaks)        # Hides specific holidays missing from your data
        ]
    ) 

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

    
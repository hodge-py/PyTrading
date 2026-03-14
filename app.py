import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import pathlib
from streamlit_searchbox import st_searchbox
import pandas_ta as ta
import plotly.graph_objects as go
from streamlit_local_storage import LocalStorage
from pystock import pyStock

localS = LocalStorage()

Stocks = pyStock()

current_watchlist = localS.getItem("my_watchlist")

st.set_page_config(
    page_title="Stock Screener & Analysis Tool",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
)

st.title("Stock Screener & Analysis Tool")

df_ticker = Stocks.load_tickers('all_tickers.txt')

#print(df_ticker)

tickerAsList = df_ticker['Companies'].tolist()

def search_tickers(search_term: str):
    if not search_term:
        return tickerAsList[:5] 
    
    # Filter the list based on what the user typed (case-insensitive)
    return [str(t) for t in tickerAsList if search_term.upper() in str(t).upper()]

#print(tickerAsList)

top_container = st.container()

col1, col2, col3 = top_container.columns([4,1,2])

with col1:
    selected_ticker = st_searchbox(
    search_function=search_tickers,
    placeholder="Search for a stock ticker... Ex. AAPL MSFT GOOGL",
    key="ticker_searchbox",
)

with col2:
    search_clicked = st.button("Search")

with col3:
    search_add = st.button("⭐ Add to Watchlist")

if search_clicked and selected_ticker:
    stockContainer = st.container(border=True)
    stockContainer.header(f"Results for {selected_ticker}")

    tick = Stocks.ticker_assign(selected_ticker)
    
    # This is where you'd put your yfinance / Plotly code
    stockContainer.info(f"Fetching live data for {selected_ticker}... {tick.info['longName']}... Industry: {tick.info['industry']}... Sector: {tick.info['sector']}...")    

    df = Stocks.stock_history()

    df_fund = Stocks.calculate_fundamentals()

    df_tech = Stocks.calculate_technicals()

    sma_df = Stocks.sma_strategy()

    stockContainer.metric(label=f"{selected_ticker} - {tick.info['longName']} - Stock Price", value=f"${df['Close'].iloc[-1]:,.2f}")

    figLine = go.Figure()
    figLine.add_trace(go.Scatter(x=df.index, y=sma_df['SMA 20'], name="SMA 20", mode='lines'))
    figLine.add_trace(go.Scatter(x=df.index, y=sma_df['SMA 50'], name="SMA 50", mode='lines'))
    figLine.add_trace(go.Scatter(x=df.index, y=sma_df['Close'], name="Close", mode='lines'))
    figLine.update_xaxes(rangeslider_visible=True)

    stockContainer.plotly_chart(figLine)

    fund_container = st.container(border=True)
    fund_container.header("Fundamental Metrics")

    fund_container.dataframe(df_fund,hide_index=True, key='df_fund')

    tech_container = st.container(border=True)
    tech_container.header("Technical Metrics")

    df['Close'] = df['Close'].astype(float)  # Ensure 'Close' is float for MACD calculation

    tech_container.dataframe(df_tech,hide_index=True, key='df_tech')

    news_container = st.container(border=True)
    news_container.header("News")

    news_df = Stocks.get_news()
    
    news_container.dataframe(news_df,row_height=150, hide_index=True, column_config={"Link": st.column_config.LinkColumn("Website Link")}, key='news_df')



elif search_clicked and not selected_ticker:
    st.warning("Please select a ticker from the list first!")

if search_add and selected_ticker:
    selected_ticker = selected_ticker.upper()

    updated_list = current_watchlist if current_watchlist else []

    if selected_ticker in updated_list:
        st.warning(f"{selected_ticker} already exists in watchlist!")
    else:
        updated_list.append(selected_ticker)
        
        # Save it back to the browser's local storage
        localS.setItem("my_watchlist", updated_list)
        st.success(f"{selected_ticker} added to watchlist!")


st.markdown("---")
st.caption("""
**Disclaimer:** This application is for **informational and educational purposes only** and does 
not constitute financial, investment, or legal advice. Investing in stocks involves 
significant risk, and past performance is **not indicative of future results**. 

The data provided is sourced from third-party APIs and may be delayed or inaccurate. 
The developer is not responsible for any financial losses or damages resulting from 
the use of this tool. Always consult with a **certified financial advisor** before 
making investment decisions.
""")
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas_ta as ta
from streamlit_local_storage import LocalStorage
from pystock import pyStock

Stocks = pyStock()
localS = LocalStorage()

st.title("My Watchlist")

col1, col2, col3 = st.columns([3,1,3], vertical_alignment='bottom')

try:
    reading_watchlist = localS.getItem("my_watchlist")
    if reading_watchlist:
        reading_watchlist = pd.DataFrame(reading_watchlist, columns=['Ticker'])
    elif reading_watchlist is None:
        raise pd.errors.EmptyDataError
    else:
        #reading_watchlist = pd.read_csv('watchlist.csv', header=None)
        raise pd.errors.EmptyDataError
        

    #print(reading_watchlist.head())
    df_fund = pd.DataFrame(columns=['Fundamental','Value'])

    df_techical = pd.DataFrame(columns=['Technical','Value'])

    with col1:
        selected_ticker = st.selectbox("Select a stock ticker to view your watchlist", options=reading_watchlist['Ticker'].tolist())

    with col2:
        search = st.button("Search")

    with col3:
        delete_from_watchlist = st.button("Remove from Watchlist")

    if delete_from_watchlist:
        reading_watchlist = reading_watchlist.replace(to_replace=selected_ticker, value=np.nan).dropna()
        reading_watchlist = reading_watchlist.reset_index(drop=True)
        reading_list = reading_watchlist['Ticker'].tolist()
        localS.setItem("my_watchlist", reading_list)
        st.success(f"{selected_ticker} removed from watchlist!")
        time.sleep(1)
        st.rerun()

    if search and selected_ticker:
        st.header(f"Results for {selected_ticker}")

        tick = Stocks.ticker_assign(selected_ticker)
        
        # This is where you'd put your yfinance / Plotly code
        st.info(f"Fetching live data for {selected_ticker}... {tick.info['longName']}... Industry: {tick.info['industry']}... Sector: {tick.info['sector']}...")    
        st.markdown("---")

        df = Stocks.stock_history()

        df_fund = Stocks.calculate_fundamentals()

        df_tech = Stocks.calculate_technicals()

        sma_df = Stocks.sma_strategy()

        st.metric(label=f"{selected_ticker} - {tick.info['longName']} - Stock Price", value=f"${df['Close'].iloc[-1]:,.2f}")

        figLine = go.Figure()
        figLine.add_trace(go.Scatter(x=df.index, y=sma_df['Close'], name="Close", mode='lines'))
        figLine.add_trace(go.Scatter(x=df.index, y=sma_df['SMA 20'], name="SMA 20", mode='lines'))
        figLine.add_trace(go.Scatter(x=df.index, y=sma_df['SMA 50'], name="SMA 50", mode='lines'))
        figLine.update_xaxes(rangeslider_visible=True)

        st.plotly_chart(figLine)

        st.markdown("---")
        
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
            ],
            rangeslider_visible=True
        ) 

        info = tick.info

        st.plotly_chart(fig)

        st.header("Fundamental Metrics")
        st.markdown("---")

        st.dataframe(df_fund,hide_index=True, key='df_fund')

        st.header("Technical Metrics")
        st.markdown("---")
        df['Close'] = df['Close'].astype(float)  # Ensure 'Close' is float for MACD calculation

        st.dataframe(df_tech,hide_index=True, key='df_tech')

        st.header("News")
        st.markdown("---")

        news_df = Stocks.get_news()
        
        st.dataframe(news_df,row_height=150, hide_index=True, column_config={"Link": st.column_config.LinkColumn("Website Link")}, key='news_df')

            


except pd.errors.EmptyDataError:
    st.warning("Your watchlist is currently empty. Please add some tickers to view them here.")
    reading_watchlist = pd.DataFrame()


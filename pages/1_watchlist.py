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
from plotly.subplots import make_subplots

Stocks = pyStock()
localS = LocalStorage()

st.set_page_config(
    page_title="Watchlist",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
)

st.title("My Watchlist")

col1, col2, col3 = st.columns([6,1,2], vertical_alignment='bottom')

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
        delete_from_watchlist = st.button("Remove from Watchlist ❌")

    if delete_from_watchlist:
        reading_watchlist = reading_watchlist.replace(to_replace=selected_ticker, value=np.nan).dropna()
        reading_watchlist = reading_watchlist.reset_index(drop=True)
        reading_list = reading_watchlist['Ticker'].tolist()
        localS.setItem("my_watchlist", reading_list)
        st.success(f"{selected_ticker} removed from watchlist!")
        time.sleep(1)
        st.rerun()

    if search and selected_ticker:

        tick = Stocks.ticker_assign(selected_ticker)

        main_container = st.container(border=True,)

        main_container.header(f"Results for {selected_ticker}")
        
        # This is where you'd put your yfinance / Plotly code
        main_container.info(f"Fetching live data for {selected_ticker}... {tick.info['longName']}... Industry: {tick.info['industry']}... Sector: {tick.info['sector']}...")    

        df = Stocks.stock_history()

        df_fund = Stocks.calculate_fundamentals()

        df_tech = Stocks.calculate_technicals()

        sma_df = Stocks.sma_strategy()

        main_container.metric(label=f"{selected_ticker} - {tick.info['longName']} - Stock Price", value=f"${df['Close'].iloc[-1]:,.2f}")
        
        fig = make_subplots(rows=1, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[1])

        fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],name="Close"), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=sma_df['SMA 20'], name="SMA 20", mode='lines'), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=sma_df['SMA 50'], name="SMA 50", mode='lines'), row=1, col=1)

        dt_all = pd.date_range(start=df.index.min(), end=df.index.max())

        # 2. Identify which dates are NOT in your actual data
        dt_obs = pd.to_datetime(df.index)
        dt_breaks = [d.strftime("%Y-%m-%d") for d in dt_all if d not in dt_obs]

        fig.update_xaxes(rangeslider_visible=True, col=1, row=1, rangebreaks=[dict(values=dt_breaks)])

        main_container.plotly_chart(fig)

        fund_container = st.container(border=True)

        fund_container.header("Fundamental Metrics")

        fund_container.dataframe(df_fund,hide_index=True, key='df_fund')

        tech_container = st.container(border=True)
        tech_container.header("Technical Metrics")
        tech_container.markdown("---")
        df['Close'] = df['Close'].astype(float)  # Ensure 'Close' is float for MACD calculation

        tech_container.dataframe(df_tech,hide_index=True, key='df_tech')

        news_container = st.container(border=True)
        news_container.header("News")
        news_container.markdown("---")

        news_df = Stocks.get_news()
        
        news_container.dataframe(news_df,row_height=150, hide_index=True, column_config={"Link": st.column_config.LinkColumn("Website Link")}, key='news_df')



except pd.errors.EmptyDataError:
    st.warning("Your watchlist is currently empty. Please add some tickers to view them here.")
    reading_watchlist = pd.DataFrame()


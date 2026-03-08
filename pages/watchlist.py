import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import time

col1, col2, col3 = st.columns([3,1,3], vertical_alignment='bottom')

try:
    reading_watchlist = pd.read_csv('watchlist.csv', header=None)


    with col1:
        selected_ticker = st.selectbox("Select a stock ticker to view your watchlist", options=reading_watchlist[0].tolist())

    with col2:
        search = st.button("Search")

    with col3:
        delete_from_watchlist = st.button("Remove from Watchlist")

    if delete_from_watchlist:
        reading_watchlist = reading_watchlist.replace(to_replace=selected_ticker, value=np.nan).dropna()
        reading_watchlist.to_csv('watchlist.csv', index=False, header=False)
        st.success(f"{selected_ticker} removed from watchlist!")
        time.sleep(1)
        st.rerun()

    if search and selected_ticker:
        st.subheader(f"Results for {selected_ticker}")
        
        # This is where you'd put your yfinance / Plotly code
        st.info(f"Fetching live data for {selected_ticker}...")

        
        df = yf.Ticker(selected_ticker).history(period='1y')

        # 1. Native Streamlit Line Chart
        st.line_chart(df['Close'])

        # 2. Interactive Plotly Chart
        import plotly.express as px
        fig = px.line(df, x=df.index, y='Close', title=f"{selected_ticker} Closing Price Over the Last Year")
        st.plotly_chart(fig)


except pd.errors.EmptyDataError:
    st.warning("Your watchlist is currently empty. Please add some tickers to view them here.")
    reading_watchlist = pd.DataFrame()


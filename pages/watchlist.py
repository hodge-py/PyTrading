import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import talib as ta

st.title("My Watchlist")

col1, col2, col3 = st.columns([3,1,3], vertical_alignment='bottom')

try:
    reading_watchlist = pd.read_csv('watchlist.csv', header=None)

    df_fund = pd.DataFrame(columns=['Fundamental','Value'])

    df_techical = pd.DataFrame(columns=['Technical','Value'])

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

        tick = yf.Ticker(selected_ticker)
        
        # This is where you'd put your yfinance / Plotly code
        st.info(f"Fetching live data for {selected_ticker}... {tick.info['longName']}...")

        
        df = tick.history(period='5y').dropna()  # Drop rows with NaN values to avoid issues with plotting
        # 2. Interactive Plotly Chart

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                    vertical_spacing=0.05, 
                    row_heights=[0.7, 0.3])
        
        fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name="Close", mode='lines'), row=1, col=1)

        fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name="Volume"), row=2, col=1)

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

        st.plotly_chart(fig)

        df_fund.loc[len(df_fund)] = ['Market Cap', str(format(tick.info.get('marketCap', 'N/A'), ',.0f'))]
        df_fund.loc[len(df_fund)] = ['PE Ratio', str(tick.info.get('trailingPE', 'N/A'))]
        df_fund.loc[len(df_fund)] = ['Price to Earnings', str(tick.info.get('priceToEarnings', 'N/A'))]
        df_fund.loc[len(df_fund)] = ['Current Ratio', str(tick.info.get('currentRatio', 'N/A'))]
        df_fund.loc[len(df_fund)] = ['Debt to Equity Ratio', str(tick.info.get('debtToEquity', 'N/A'))]
        df_fund.loc[len(df_fund)] = ['Return on Equity', str(tick.info.get('returnOnEquity', 'N/A'))]
        df_fund.loc[len(df_fund)] = ['Earnings Per Share', str(tick.info.get('earningsPerShare', 'N/A'))]
        df_fund.loc[len(df_fund)] = ['Price to Book', str(tick.info.get('priceToBook', 'N/A'))]
        df_fund.loc[len(df_fund)] = ['Beta', str(tick.info.get('beta', 'N/A'))]
        df_fund.loc[len(df_fund)] = ['52 Week High', str(tick.info.get('fiftyTwoWeekHigh', 'N/A'))]
        df_fund.loc[len(df_fund)] = ['52 Week Low', str(tick.info.get('fiftyTwoWeekLow', 'N/A'))]
        df_fund.loc[len(df_fund)] = ['Forward PE', str(tick.info.get('forwardPE', 'N/A'))]

        st.subheader("Fundamental Metrics")

        st.dataframe(df_fund,hide_index=True, key='df_fund')

        st.subheader("Technical Metrics")

        sma_20 = ta.SMA(df['Close'], timeperiod=20).iloc[-1]
        sma_50 = ta.SMA(df['Close'], timeperiod=50).iloc[-1]
        rsi_14 = ta.RSI(df['Close'], timeperiod=14).iloc[-1]
        macd, macd_signal, macd_hist = ta.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)

        df_techical.loc[len(df_techical)] = ['SMA 20', str(round(sma_20,2))]
        df_techical.loc[len(df_techical)] = ['SMA 50', str(round(sma_50,2))]
        df_techical.loc[len(df_techical)] = ['RSI 14', str(round(rsi_14,2))]
        df_techical.loc[len(df_techical)] = ['MACD', str(round(macd.iloc[-1],2))]
        df_techical.loc[len(df_techical)] = ['MACD Signal', str(round(macd_signal.iloc[-1],2))]
        df_techical.loc[len(df_techical)] = ['MACD Histogram', str(round(macd_hist.iloc[-1],2))]
        df_techical.loc[len(df_techical)] = ['Close Price', str(round(df['Close'].iloc[-1],2))]
        df_techical.loc[len(df_techical)] = ['Volume', str(format(round(df['Volume'].iloc[-1],2), ',.0f'))]
        df_techical.loc[len(df_techical)] = ['20 Day Volatility', str(round(df['Close'].pct_change().rolling(window=20).std().iloc[-1]*100,2)) + '%']
        df_techical.loc[len(df_techical)] = ['50 Day Volatility', str(round(df['Close'].pct_change().rolling(window=50).std().iloc[-1]*100,2)) + '%']

        st.dataframe(df_techical,hide_index=True, key='df_techical')

        st.subheader("News")

        news = tick.news
        headlines = []
        summary = []
        links = []

        for i in range(len(news)):
            headlines.append(news[i]['content']['title'])
            summary.append(news[i]['content']['summary'])
            links.append(news[i]['content']['canonicalUrl']['url'])
        
        newsNew = list(zip(headlines, summary, links))
        news_df = pd.DataFrame(newsNew, columns=['Headline', 'Summary', 'Link'])
        st.dataframe(news_df,row_height=150, hide_index=True, column_config={"Link": st.column_config.LinkColumn("Website Link")}, key='news_df')




except pd.errors.EmptyDataError:
    st.warning("Your watchlist is currently empty. Please add some tickers to view them here.")
    reading_watchlist = pd.DataFrame()


import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import pathlib
from streamlit_searchbox import st_searchbox
import pandas_ta as ta
import plotly.graph_objects as go
from streamlit_local_storage import LocalStorage

localS = LocalStorage()

current_watchlist = localS.getItem("my_watchlist")

st.set_page_config(
    page_title="Stock Screener & Analysis Tool",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
)

st.title("Stock Screener & Analysis Tool")

df_fund = pd.DataFrame(columns=['Fundamental','Value'])

df_techical = pd.DataFrame(columns=['Technical','Value'])


df_ticker = pd.read_csv('all_tickers.txt', sep='\t', header=0)

#print(df_ticker)

tickerAsList = df_ticker['Companies'].tolist()

def search_tickers(search_term: str):
    if not search_term:
        return tickerAsList[:5] 
    
    # Filter the list based on what the user typed (case-insensitive)
    return [str(t) for t in tickerAsList if search_term.upper() in str(t).upper()]

#print(tickerAsList)

col1, col2, col3 = st.columns([4,1,2])

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
    st.header(f"Results for {selected_ticker}")
    

    tick = yf.Ticker(selected_ticker)
    
    # This is where you'd put your yfinance / Plotly code
    st.info(f"Fetching live data for {selected_ticker}... {tick.info['longName']}... Industry: {tick.info['industry']}... Sector: {tick.info['sector']}...")    
    st.markdown("---")
    df = tick.history(period='5y').dropna()  # Drop rows with NaN values to avoid issues with plotting
    
    # 1. Native Streamlit Line Chart
    sma_20 = ta.sma(df['Close'], timeperiod=20)
    sma_50 = ta.sma(df['Close'], timeperiod=50)
    df['sma_20'] = sma_20
    df['sma_50'] = sma_50

    st.metric(label=f"{selected_ticker} - {tick.info['longName']} - Stock Price", value=f"${df['Close'].iloc[-1]:,.2f}")

    figLine = go.Figure()
    figLine.add_trace(go.Scatter(x=df.index, y=df['Close'], name="Close", mode='lines'))
    figLine.add_trace(go.Scatter(x=df.index, y=df['sma_20'], name="SMA 20", mode='lines'))
    figLine.add_trace(go.Scatter(x=df.index, y=df['sma_50'], name="SMA 50", mode='lines'))
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

    st.plotly_chart(fig)

    df_fund.loc[len(df_fund)] = ['Market Cap', str(format(tick.info.get('marketCap', 'N/A'), ',.0f')) if tick.info.get('marketCap', 'N/A') != 'N/A' else 'N/A']
    df_fund.loc[len(df_fund)] = ['PE Ratio', str(round(tick.info.get('trailingPE', 'N/A'), 2)) if tick.info.get('trailingPE', 'N/A') != 'N/A' else 'N/A']
    df_fund.loc[len(df_fund)] = ['Price to Earnings', str(round(tick.info.get('priceToEarnings', 'N/A'), 2)) if tick.info.get('priceToEarnings', 'N/A') != 'N/A' else 'N/A']
    df_fund.loc[len(df_fund)] = ['Current Ratio', str(round(tick.info.get('currentRatio', 'N/A'), 2)) if tick.info.get('currentRatio', 'N/A') != 'N/A' else 'N/A']
    df_fund.loc[len(df_fund)] = ['Debt to Equity Ratio', str(round(tick.info.get('debtToEquity', 'N/A'), 2)) if tick.info.get('debtToEquity', 'N/A') != 'N/A' else 'N/A']
    df_fund.loc[len(df_fund)] = ['Return on Equity', str(round(tick.info.get('returnOnEquity', 'N/A'), 2)) if tick.info.get('returnOnEquity', 'N/A') != 'N/A' else 'N/A']
    df_fund.loc[len(df_fund)] = ['Earnings Per Share', str(round(tick.info.get('earningsPerShare', 'N/A'), 2)) if tick.info.get('earningsPerShare', 'N/A') != 'N/A' else 'N/A']
    df_fund.loc[len(df_fund)] = ['Price to Book', str(round(tick.info.get('priceToBook', 'N/A'), 2)) if tick.info.get('priceToBook', 'N/A') != 'N/A' else 'N/A']
    df_fund.loc[len(df_fund)] = ['Beta', str(round(tick.info.get('beta', 'N/A'), 2)) if tick.info.get('beta', 'N/A') != 'N/A' else 'N/A']
    df_fund.loc[len(df_fund)] = ['52 Week High', str(round(tick.info.get('fiftyTwoWeekHigh', 'N/A'), 2)) if tick.info.get('fiftyTwoWeekHigh', 'N/A') != 'N/A' else 'N/A']
    df_fund.loc[len(df_fund)] = ['52 Week Low', str(round(tick.info.get('fiftyTwoWeekLow', 'N/A'), 2)) if tick.info.get('fiftyTwoWeekLow', 'N/A') != 'N/A' else 'N/A']
    df_fund.loc[len(df_fund)] = ['Forward PE', str(round(tick.info.get('forwardPE', 'N/A'), 2)) if tick.info.get('forwardPE', 'N/A') != 'N/A' else 'N/A']

    st.header("Fundamental Metrics")
    st.markdown("---")

    st.dataframe(df_fund,hide_index=True, key='df_fund')

    st.header("Technical Metrics")
    st.markdown("---")
    df['Close'] = df['Close'].astype(float)  # Ensure 'Close' is float for MACD calculation
    sma_20 = ta.sma(df['Close'], timeperiod=20).iloc[-1]
    sma_50 = ta.sma(df['Close'], timeperiod=50).iloc[-1]
    rsi_14 = ta.rsi(df['Close'], timeperiod=14).iloc[-1]
    
    macd = ta.macd(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)

    if macd is not None and len(macd) > 0:
        macd_line = macd.iloc[-1, 0]  # MACD Line
        signal_line = macd.iloc[-1, 1]  # Signal Line
        histogram = macd.iloc[-1, 2]    # MACD Histogram
    else:
        macd_line = signal_line = histogram = np.nan  # Handle case where MACD couldn't be calculated

    df_techical.loc[len(df_techical)] = ['SMA 20', str(round(sma_20,2))]
    df_techical.loc[len(df_techical)] = ['SMA 50', str(round(sma_50,2))]
    df_techical.loc[len(df_techical)] = ['RSI 14', str(round(rsi_14,2))]
    df_techical.loc[len(df_techical)] = ['MACD', str(round(macd_line,2))]
    df_techical.loc[len(df_techical)] = ['MACD Signal', str(round(signal_line,2))]
    df_techical.loc[len(df_techical)] = ['MACD Histogram', str(round(histogram,2))]
    df_techical.loc[len(df_techical)] = ['Close Price', str(round(df['Close'].iloc[-1],2))]
    df_techical.loc[len(df_techical)] = ['Volume', str(format(round(df['Volume'].iloc[-1],2), ',.0f'))]
    df_techical.loc[len(df_techical)] = ['20 Day Volatility', str(round(df['Close'].pct_change().rolling(window=20).std().iloc[-1]*100,2)) + '%']
    df_techical.loc[len(df_techical)] = ['50 Day Volatility', str(round(df['Close'].pct_change().rolling(window=50).std().iloc[-1]*100,2)) + '%']

    st.dataframe(df_techical,hide_index=True, key='df_techical')

    st.header("News")
    st.markdown("---")

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
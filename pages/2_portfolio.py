import time

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from streamlit_local_storage import LocalStorage
from pystock import pyStock
from streamlit_searchbox import st_searchbox

ls = LocalStorage()

Stocks = pyStock()

st.set_page_config(
    page_title="My Portfolio",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
)

df = pd.DataFrame(columns=['Ticker', 'Shares Owned', 'Average Share Price', 'Original Value' , 'Current Share Price', 'Current Value', 'Gain/Loss', 'Gain/Loss %'])

My_Portfolio = ls.getItem("my_portfolio")

if My_Portfolio:
    df = pd.DataFrame(My_Portfolio)
    for index, row in df.iterrows():
        ticker = row['Ticker']
        shares_owned = int(row['Shares Owned'])
        avg_share_price = float(row['Average Share Price'].replace('$', ''))
        Stocks.ticker_assign(ticker)
        stockPrice = Stocks.get_info().get('currentPrice', None)
        df.at[index, 'Current Share Price'] = "${:.2f}".format(stockPrice) if stockPrice else stockPrice
        df.at[index, 'Current Value'] = "${:.2f}".format(stockPrice * shares_owned) if stockPrice else stockPrice
        df.at[index, 'Gain/Loss'] = f"${(stockPrice - avg_share_price) * shares_owned:.2f}"
        df.at[index, 'Gain/Loss %'] = f"{((stockPrice - avg_share_price) / avg_share_price) * 100 if avg_share_price > 0 else 0:.2f}%"

ticker_list = Stocks.load_tickers('all_tickers.txt')['Companies'].tolist()

def search_tickers(search_term: str):
    if not search_term:
        return ticker_list[:5] 
    
    # Filter the list based on what the user typed (case-insensitive)
    return [str(t) for t in ticker_list if search_term.upper() in str(t).upper()]

def handle_deletion_callback():
    # Get the indices of the deleted rows from session state
    deleted_indices = st.session_state["my_portfolio"]["deleted_rows"]
    
    # Update the actual dataframe in session state by dropping the rows

    df.drop(index=deleted_indices, inplace=True)

    # Update the dataframe in local storage
    ls.setItem("my_portfolio", df.to_dict(orient='records'))

st.title("My Portfolio")

c = st.container(border=True)

col1, col2, col3, col4 = c.columns([1,1,1,1], vertical_alignment='bottom')

with col1:
    selected_ticker = st_searchbox(
        label="Select a stock ticker to view your portfolio",
        search_function=search_tickers,
        key="ticker_search"
    )

with col2:
    sharesInput = st.number_input("Shares Owned", min_value=0, step=1, key="shares_input")

with col3:
    avg_share_price = st.number_input("Average Share Price", min_value=0.0, step=0.01, key="avg_price_input")

with col4:
    add_to_portfolio = st.button("Add to Portfolio")

valCol1, valCol2, valCol3 = st.columns([1,1,1], vertical_alignment='center',border=True)

with valCol1:
    portfolio_value = df['Current Value'].replace('[\\$,]', '', regex=True).astype(float).sum()
    st.metric(label="Total Portfolio Value", value=f"${portfolio_value:,.2f}")

with valCol2:
    total_gain_loss = df['Gain/Loss'].replace('[\\$,]', '', regex=True).astype(float).sum()
    st.metric(label="Total Gain/Loss", value=f"${total_gain_loss:,.2f}")

with valCol3:
    total_gain_loss_percent = df['Gain/Loss %'].replace('[\\%,]', '', regex=True).astype(float).sum()
    st.metric(label="Total Gain/Loss %", value=f"{total_gain_loss_percent:.2f}%")

c_table = st.container(border=True)

c_table.data_editor(df, num_rows="dynamic", use_container_width='stretch', key="my_portfolio",on_change=handle_deletion_callback,column_config={'Ticker': {'alignment':'center'}, 'Shares Owned': {'alignment':'right'}, 'Average Share Price': {'alignment':'right'}, 'Current Share Price': {'alignment':'right'}, 'Gain/Loss': {'alignment':'right'}, 'Gain/Loss %': {'alignment':'right'}, 'Original Value': {'alignment':'right'}, 'Current Value': {'alignment':'right'} })


if add_to_portfolio and selected_ticker:

    Stocks.ticker_assign(selected_ticker)
    stockPrice = Stocks.get_info().get('currentPrice', None)
    new_entry = {
        'Ticker': selected_ticker,
        'Shares Owned': str(sharesInput),
        'Average Share Price': "${:.2f}".format(avg_share_price) if avg_share_price else avg_share_price,
        'Original Value': "${:.2f}".format(sharesInput * avg_share_price) if avg_share_price else avg_share_price,
        'Current Share Price': "${:.2f}".format(stockPrice) if stockPrice else stockPrice,
        'Current Value': "${:.2f}".format(stockPrice * sharesInput) if stockPrice else stockPrice,
        'Gain/Loss': f"${(stockPrice - avg_share_price) * sharesInput:.2f}",
        'Gain/Loss %': f"{((stockPrice - avg_share_price) / avg_share_price) * 100 if avg_share_price > 0 else 0:.2f}%",
    }

    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    ls.setItem("my_portfolio", df.to_dict(orient='records'))
    st.success(f"{selected_ticker} added to portfolio!")
    time.sleep(1)
    st.rerun()






import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np


def get_data(ticker):
    data = yf.Ticker(ticker)
    hist = data.history(period="1y")
    return hist

st.title("Stock Price Visualization")

ticker = st.text_input("Enter a stock ticker symbol:", "AAPL")
if ticker:
    data = get_data(ticker)
    st.line_chart(data['Close'])

            
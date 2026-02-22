#Fundamental for general direction and technical for more fine tuned entry and position closing
import pathlib
import pandas as pd
import numpy as np
import yfinance as yf
import talib
import mplfinance as mpf

df = pd.read_csv('all_tickers.txt', sep='\t')
main_df = pd.DataFrame(columns=['Ticker', 'Price', 'SMA_20', 'SMA_50', 'RSI'])

print(df.head())

for index, row in df.iterrows():
    print(row)
    ticker = row.iloc[0]  # Assuming the ticker is in the first column
    print(f"Processing {ticker}...")
    
    # Fetch historical data for the ticker
    try:
        data = yf.Ticker(ticker)
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        continue

    dataHistory = data.history(period="1y")  # Fetch 1 year of historical data
    
    # Calculate technical indicators using TA-Lib
    main_df['SMA_20'] = talib.SMA(dataHistory['Close'], timeperiod=20)
    main_df['SMA_50'] = talib.SMA(dataHistory['Close'], timeperiod=50)
    main_df['RSI'] = talib.RSI(dataHistory['Close'], timeperiod=14)
    
    # Save the processed data to a new CSV file
    output_path = pathlib.Path(f"{ticker}_processed.csv")
    main_df.to_csv(output_path)
    
    print(f"Finished processing {ticker}. Data saved to {output_path}\n")
    print(index,row)
    break
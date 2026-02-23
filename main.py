#Fundamental for general direction and technical for more fine tuned entry and position closing
import pathlib
import pandas as pd
import numpy as np
import yfinance as yf
import talib
import mplfinance as mpf

df = pd.read_csv('all_tickers.txt', sep='\t')
main_df = pd.DataFrame(columns=['Ticker', 'Price', 'SMA_20', 'SMA_50', 'RSI', 'Current Ratio', 'Debt to Equity Ratio', 'Return on Equity', 'Earnings Per Share', 'Price to Earnings Ratio', 'Price to Book Ratio', 'quickRatio'])
final_df = pd.DataFrame(columns=['Ticker', 'Price', 'SMA_20', 'SMA_50', 'RSI', 'Current Ratio', 'Debt to Equity Ratio', 'Return on Equity', 'Earnings Per Share', 'Price to Earnings Ratio', 'Price to Book Ratio', 'quickRatio'])

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
    main_df['SMA_20'] = talib.SMA(dataHistory['Close'], timeperiod=20)  # Get the last value of SMA_20
    main_df['SMA_50'] = talib.SMA(dataHistory['Close'], timeperiod=50)  # Get the last value of SMA_50
    main_df['RSI'] = talib.RSI(dataHistory['Close'], timeperiod=14)  # Get the last value of RSI
    main_df['Price'] = dataHistory['Close'].iloc[-1]  # Get the last closing price
    main_df['Ticker'] = ticker

    main_df['SMA_20'] = main_df['SMA_20'].iloc[-1]
    main_df['SMA_50'] = main_df['SMA_50'].iloc[-1]
    main_df['RSI'] = main_df['RSI'].iloc[-1]

    main_df['Current Ratio'] = data.get_info().get('currentRatio', np.nan)  # Use .get() to avoid KeyError if the key is missing
    main_df['Debt to Equity Ratio'] = data.get_info().get('debtToEquity', np.nan)
    main_df['Return on Equity'] = data.get_info().get('returnOnEquity', np.nan)
    main_df['Earnings Per Share'] = data.get_info().get('earningsPerShare', np.nan)
    main_df['Price to Earnings Ratio'] = data.get_info().get('trailingEps', np.nan)
    main_df['Price to Book Ratio'] = data.get_info().get('priceToBook', np.nan)
    main_df['Price to Cash Flow Ratio'] = data.get_info().get('priceToCashflow', np.nan)

    main_df = main_df[['Ticker', 'Price', 'SMA_20', 'SMA_50', 'RSI', 'Current Ratio', 'Debt to Equity Ratio', 'Return on Equity', 'Earnings Per Share', 'Price to Earnings Ratio', 'Price to Book Ratio', 'quickRatio']].iloc[-1:]  # Keep only the last row for the current ticker

    # Save the processed data to a new CSV file
    print(main_df)
    final_df = pd.concat([final_df, main_df], ignore_index=True)
    
    print(data.get_info())
    
    if index >= 30:  # Limit to processing the first 10 tickers for testing
        break

output_path = pathlib.Path(f"Tickers_processed.csv")
final_df.to_csv(output_path)
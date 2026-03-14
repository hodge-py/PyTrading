import pandas as pd
import yfinance as yf
import pandas_ta as ta

class pyStock:

    def __init__(self):
        self.data = pd.DataFrame()
        self.ticker = None
        self.df_fund = pd.DataFrame(columns=['Fundamental','Value', 'Sector Avg'])
        self.df_tech = pd.DataFrame(columns=['Technical','Value'])
        self.df_ticker = ''
        self.sector_averages = {
    "Technology": {
        "avg_pe_fwd": 31.2,
        "avg_current_ratio": 2.10,
        "avg_debt_to_equity": 0.35,
        "avg_return_on_equity": 0.28,
        "avg_earnings_per_share": 5.50,
        "avg_price_to_book": 8.50,
        "avg_beta": 1.25
    },
    "Financial Services": {
        "avg_pe_fwd": 14.5,
        "avg_current_ratio": 1.50,
        "avg_debt_to_equity": 0.90,
        "avg_return_on_equity": 0.14,
        "avg_earnings_per_share": 4.20,
        "avg_price_to_book": 1.40,
        "avg_beta": 1.10
    },
    "Healthcare": {
        "avg_pe_fwd": 21.0,
        "avg_current_ratio": 2.80,
        "avg_debt_to_equity": 0.55,
        "avg_return_on_equity": 0.18,
        "avg_earnings_per_share": 3.80,
        "avg_price_to_book": 4.50,
        "avg_beta": 0.85
    },
    "Energy": {
        "avg_pe_fwd": 11.5,
        "avg_current_ratio": 1.40,
        "avg_debt_to_equity": 0.65,
        "avg_return_on_equity": 0.15,
        "avg_earnings_per_share": 6.10,
        "avg_price_to_book": 1.80,
        "avg_beta": 1.05
    },
    "Consumer Cyclical": {
        "avg_pe_fwd": 24.0,
        "avg_current_ratio": 1.70,
        "avg_debt_to_equity": 1.10,
        "avg_return_on_equity": 0.22,
        "avg_earnings_per_share": 4.50,
        "avg_price_to_book": 5.80,
        "avg_beta": 1.20
    }
}
        
    def load_tickers(self, filepath):
        self.df_ticker = pd.read_csv(filepath, sep='\t', header=0)
        return self.df_ticker
    
    def ticker_assign(self, ticker):
        self.ticker = yf.Ticker(ticker)
        return self.ticker
    
    def stock_history(self):
        self.data = self.ticker.history(period="5y").dropna()
        return self.data
    
    def calculate_fundamentals(self):
        info = self.ticker.info
        sector = info.get('sector', 'Unknown')
        market_cap = f"${info.get('marketCap', 'N/A'):,}" if info.get('marketCap', None) else 'N/A'
        pe_fwd = info.get('forwardPE', None)
        current_ratio = info.get('currentRatio', None)
        debt_to_equity = info.get('debtToEquity', None)
        return_on_equity = info.get('returnOnEquity', None)
        earnings_per_share = info.get('earningsPerShare', None)
        price_to_book = info.get('priceToBook', None)
        beta = info.get('beta', None)

        self.df_fund = pd.DataFrame({
            'Fundamental': ['Market Cap', 'Forward P/E', 'Current Ratio', 'Debt to Equity', 'Return on Equity', 'Earnings Per Share', 'Price to Book', 'Beta'],
            'Value': [market_cap, pe_fwd, current_ratio, debt_to_equity, return_on_equity, earnings_per_share, price_to_book, beta],
            'Sector Avg': [
                self.sector_averages.get(sector, {}).get('avg_market_cap'),
                self.sector_averages.get(sector, {}).get('avg_pe_fwd'),
                self.sector_averages.get(sector, {}).get('avg_current_ratio'),
                self.sector_averages.get(sector, {}).get('avg_debt_to_equity'),
                self.sector_averages.get(sector, {}).get('avg_return_on_equity'),
                self.sector_averages.get(sector, {}).get('avg_earnings_per_share'),
                self.sector_averages.get(sector, {}).get('avg_price_to_book'),
                self.sector_averages.get(sector, {}).get('avg_beta')
            ]
        })
        return self.df_fund
    
    def calculate_technicals(self):
        sma_20 = ta.sma(self.data['Close'], timeperiod=20)
        sma_50 = ta.sma(self.data['Close'], timeperiod=50)
        rsi_14 = ta.rsi(self.data['Close'], timeperiod=14)
        macd = ta.macd(self.data['Close'], fastperiod=12, slowperiod=26, signalperiod=9)

        self.df_tech = pd.DataFrame({
            'Technical': ['SMA 20', 'SMA 50', 'RSI 14', 'MACD', 'MACD Signal', 'MACD Hist'],
            'Value': [sma_20.iloc[-1], sma_50.iloc[-1], rsi_14.iloc[-1], macd.iloc[-1,0], macd.iloc[-1,1], macd.iloc[-1,2]]
        })
        return self.df_tech
    
    def sma_strategy(self):
        self.data['SMA 20'] = ta.sma(self.data['Close'], timeperiod=20)
        self.data['SMA 50'] = ta.sma(self.data['Close'], timeperiod=50)
        self.data['Signal'] = 0
        self.data.loc[self.data['SMA 20'] > self.data['SMA 50'], 'Signal'] = 1
        self.data.loc[self.data['SMA 20'] < self.data['SMA 50'], 'Signal'] = -1
        return self.data[['Close', 'SMA 20', 'SMA 50', 'Signal']]
    
    def get_news(self):
        news = self.ticker.news
        headlines = []
        summary = []
        links = []

        for i in range(len(news)):
            headlines.append(news[i]['content']['title'])
            summary.append(news[i]['content']['summary'])
            links.append(news[i]['content']['canonicalUrl']['url'])
        
        newsNew = list(zip(headlines, summary, links))
        news_df = pd.DataFrame(newsNew, columns=['Headline', 'Summary', 'Link'])
        return news_df
    
    def get_info(self):
        return self.ticker.info

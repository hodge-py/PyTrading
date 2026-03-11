# 📈 Streamlit Stock Tracker & Watchlist

A sleek, lightweight web application built with Streamlit that allows investors to track real-time market data, visualize price trends, and maintain a personalized watchlist.

### ✨ Features
* Real-Time Data: Fetches live market prices and historical data using the yfinance API.
* Interactive Charts: Dynamic technical analysis charts powered by Plotly.
* Personalized Watchlist: Save your favorite tickers to a persistent list for quick monitoring.
* Key Metrics: View Market Cap, P/E Ratio, 52-week highs/lows, and dividend yields at a glance.

---

### 🛠️ Tech Stack
* Frontend: Streamlit
* Data Source: yfinance
* Visualization: Plotly / Matplotlib
* Data Handling: Pandas & NumPy

---

### 🚀 Getting Started

#### 1. Download Docker Desktop

https://docs.docker.com/get-started/introduction/get-docker-desktop/

#### 2. Create a Folder and Inside Download the Docker Compose File

<a href='https://docs.docker.com/get-started/introduction/get-docker-desktop/' download>docker-compose.yml</a>

#### 3. Pull the Docker Image

```terminal
docker-compose pull
```

#### 4. Run the Image

```terminal
docker-compose up -d
```

### Updating the App

An updates can be installed by running the pull command again

```terminal
docker-compose pull
```

---

### 📂 Project Structure
* app.py              # Main Streamlit application logic
* data_utils.py       # Helper functions for API calls
* watchlist.csv       # Local storage for saved tickers
* requirements.txt    # Project dependencies
* README.md           # Project documentation

---

### 📝 How It Works
1. Search: Enter a stock ticker (e.g., AAPL, TSLA) in the sidebar.
2. Analyze: Review the historical performance and fundamental data.
3. Save: Click the "Add to Watchlist" button to store the ticker.
4. Monitor: The main dashboard provides a summary of all saved stocks.

> Note: This app currently uses a local CSV or session state for the watchlist. For production environments, consider connecting a database.

---

### 🤝 Contributing
Contributions, issues, and feature requests are welcome!

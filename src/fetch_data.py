import yfinance as yf
import pandas as pd
from datetime import date

STOCKS = {
    "Apple":      "AAPL",
    "Microsoft":  "MSFT",
    "Google":     "GOOGL",
    "Amazon":     "AMZN",
    "Meta":       "META",
    "Tesla":      "TSLA",
    "Nvidia":     "NVDA",
    "JPMorgan":   "JPM",
    "Goldman":    "GS",
    "ExxonMobil": "XOM",
    "Johnson&J":  "JNJ",
    "Berkshire":  "BRK-B",
}

def fetch_prices(period="1y"):
    tickers = list(STOCKS.values())
    print("📡 Pulling stock data from Yahoo Finance...")
    raw = yf.download(tickers, period=period, auto_adjust=True, progress=False)
    prices = raw["Close"]
    print(f"✅ Got {len(prices)} trading days of data")
    return prices

def compute_returns(prices):
    return prices.pct_change().dropna()

def compute_correlation(returns):
    return returns.corr()
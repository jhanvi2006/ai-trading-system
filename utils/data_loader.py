import pandas as pd
import streamlit as st
@st.cache_data(ttl=3600)  # Refresh live data every hour
def load_clean_data(stock):
    try:
        import yfinance as yf
        ticker_obj = yf.Ticker(stock)
        df = ticker_obj.history(period="2y", interval="1d") # 2 years is perfectly optimal for RL without slowing down speed
        df.reset_index(inplace=True)
        # Ensure date column is standard
        if "Date" not in df.columns and "Datetime" in df.columns:
            df.rename(columns={"Datetime": "Date"}, inplace=True)
            
        # Ensure timestamp is stripped to just date if we have timezone awares
        df["Date"] = pd.to_datetime(df["Date"]).dt.tz_localize(None)

    except Exception:
        # Fallback to offline CSV if API fails or no internet
        df = pd.read_csv(f"datasets/{stock}_stock_data.csv")
        df["Date"] = pd.to_datetime(df["Date"])

    # ✅ Convert columns to numeric
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
    df["Open"] = pd.to_numeric(df["Open"], errors="coerce")
    df["High"] = pd.to_numeric(df["High"], errors="coerce")
    df["Low"] = pd.to_numeric(df["Low"], errors="coerce")

    df = df.dropna()
    df = df.sort_values("Date")


    # Moving Average
    df["MA_10"] = df["Close"].rolling(window=10).mean()

    # RSI
    delta = df["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()

    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))

    df = df.dropna()

    return df
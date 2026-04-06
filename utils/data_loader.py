import pandas as pd
import streamlit as st
@st.cache_data

def load_clean_data(stock):
    df = pd.read_csv(f"datasets/{stock}_stock_data.csv")

    # ✅ Convert columns to numeric
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
    df["Open"] = pd.to_numeric(df["Open"], errors="coerce")
    df["High"] = pd.to_numeric(df["High"], errors="coerce")
    df["Low"] = pd.to_numeric(df["Low"], errors="coerce")

    df = df.dropna()

    df["Date"] = pd.to_datetime(df["Date"])
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
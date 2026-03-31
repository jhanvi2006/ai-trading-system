import yfinance as yf
import pandas as pd

ticker = "NVDA"

data = yf.download(ticker, period="5y", interval="1d")
data.reset_index(inplace=True)

data.to_csv("datasets/NVDA_stock_data.csv", index=False)

print("NVDA dataset downloaded successfully!")
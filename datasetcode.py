import yfinance as yf
import pandas as pd

# Stock ticker for NVIDIA
ticker = "NVDA"

# Download last 5 years of daily data
data = yf.download(ticker, period="5y", interval="1d")

# Reset index to make Date a column
data.reset_index(inplace=True)

# Save dataset as CSV
data.to_csv("NVDA_stock_data.csv", index=False)

print("NVDA dataset downloaded successfully!")

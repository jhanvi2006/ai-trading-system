import pandas as pd

def load_clean_data(stock):
    df = pd.read_csv(f"datasets/{stock}_stock_data.csv")

    df.columns = df.columns.str.strip()
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    for col in ['Open', 'High', 'Low', 'Close']:
        df[col] = df[col].astype(str).str.replace(',', '')
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df = df.dropna(subset=['Open', 'High', 'Low', 'Close'])
    df = df.reset_index(drop=True)

    df['MA10'] = df['Close'].rolling(window=10).mean()

    return df
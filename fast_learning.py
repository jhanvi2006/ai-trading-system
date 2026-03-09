import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
from agent import teaching_agent
from trading_engine import buy_stock, sell_stock


def run_fast_learning():

    st.title("Fast Learning Trading Simulator")

    stocks = {
        "AAPL": "datasets/AAPL_stock_data.csv",
        "NVDA": "datasets/NVDA_stock_data.csv",
        "AMZN": "datasets/AMZN_stock_data.csv",
        "MSFT": "datasets/MSFT_stock_data.csv",
        "GOOGL": "datasets/GOOGL_stock_data.csv"
    }

    st.sidebar.title("Market Selection")

    stock_choice = st.sidebar.selectbox("Select Stock", list(stocks.keys()))

    data = pd.read_csv(stocks[stock_choice])

    data["Open"] = pd.to_numeric(data["Open"], errors="coerce")
    data["High"] = pd.to_numeric(data["High"], errors="coerce")
    data["Low"] = pd.to_numeric(data["Low"], errors="coerce")
    data["Close"] = pd.to_numeric(data["Close"], errors="coerce")

    data = data.dropna()

    if "balance" not in st.session_state:
        st.session_state.balance = 100000

    if "portfolio" not in st.session_state:
        st.session_state.portfolio = {}

    if "trade_history" not in st.session_state:
        st.session_state.trade_history = []

    if "step" not in st.session_state:
        st.session_state.step = 50

    if st.session_state.step >= len(data):
        st.warning("Simulation finished")
        st.stop()

    current_data = data.iloc[:st.session_state.step]

    current_price = current_data["Close"].iloc[-1]

    fig = go.Figure(
        data=[
            go.Candlestick(
                x=current_data["Date"],
                open=current_data["Open"],
                high=current_data["High"],
                low=current_data["Low"],
                close=current_data["Close"]
            )
        ]
    )

    fig.update_layout(title=f"{stock_choice} Market Simulation")

    st.plotly_chart(fig, use_container_width=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Current Price", f"${round(current_price,2)}")

    with col2:
        st.metric("Balance", f"${round(st.session_state.balance,2)}")

    with col3:
        shares = st.session_state.portfolio.get(stock_choice, 0)
        st.metric("Shares Owned", shares)

    st.subheader("Trade")

    quantity = st.number_input("Quantity", min_value=1)

    col_buy, col_sell = st.columns(2)

    with col_buy:
        if st.button("Buy"):
            buy_stock(stock_choice, current_price, quantity)

    with col_sell:
        if st.button("Sell"):
            sell_stock(stock_choice, current_price, quantity)

    st.subheader("Teaching Agent Feedback")

    feedback = teaching_agent(current_data, st.session_state.trade_history)

    for msg in feedback:
        st.info(msg)

    st.subheader("Trade History")

    if st.session_state.trade_history:
        st.dataframe(pd.DataFrame(st.session_state.trade_history))

    st.subheader("Portfolio")

    if st.session_state.portfolio:
        st.dataframe(pd.DataFrame(
            list(st.session_state.portfolio.items()),
            columns=["Stock","Shares"]
        ))

    time.sleep(3)

    st.session_state.step += 1
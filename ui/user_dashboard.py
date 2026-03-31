import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_clean_data
from utils.charts import create_candlestick
from utils.portfolio import *


def show_user_dashboard():

    initialize_portfolio(st)

    stock = st.session_state.get('selected_stock', 'AAPL')

    # =========================
    # 🌍 MARKET OVERVIEW
    # =========================
    st.subheader("🌍 Market Overview")

    cols = st.columns(5)
    stocks = ["AAPL", "AMZN", "GOOGL", "MSFT", "NVDA"]

    for i, s in enumerate(stocks):
        df_s = load_clean_data(s)
        change = ((df_s['Close'].iloc[-1] / df_s['Close'].iloc[-2] - 1) * 100)

        with cols[i]:
            st.metric(s, f"${df_s['Close'].iloc[-1]:.2f}", f"{change:+.1f}%")

    # =========================
    # 📊 DASHBOARD
    # =========================
    st.subheader("💰 Portfolio Dashboard")

    portfolio_value = calculate_portfolio_value(st.session_state.portfolio)
    total_value = st.session_state.balance + portfolio_value
    profit = total_value - st.session_state.initial_balance
    profit_pct = (profit / st.session_state.initial_balance) * 100

    c1, c2, c3 = st.columns(3)

    c1.metric("💵 Balance", f"${st.session_state.balance:.2f}")
    c2.metric("📈 Portfolio", f"${portfolio_value:.2f}")
    c3.metric("🎯 P&L", f"${profit:.2f}", f"{profit_pct:+.1f}%")

    # =========================
    # 🥧 PORTFOLIO PIE
    # =========================
    if st.session_state.portfolio:

        holdings = {
            k: v * 100 for k, v in st.session_state.portfolio.items()
        }

        fig_pie = px.pie(values=list(holdings.values()), names=list(holdings.keys()))
        st.plotly_chart(fig_pie, use_container_width=True, key="user_pie_chart")

    # =========================
    # ⚡ TRADING
    # =========================
    st.subheader("⚡ Quick Trade")

    df = load_clean_data(stock)
    price = df['Close'].iloc[-1]

    st.metric("Current Price", f"${price:.2f}")

    col1, col2 = st.columns(2)

    if col1.button("🟢 BUY", use_container_width=True):
        buy_stock(st, stock, price)
        st.success("Bought!")
        st.rerun()

    if col2.button("🔴 SELL", use_container_width=True):
        sell_stock(st, stock, price)
        st.success("Sold!")
        st.rerun()

    # =========================
    # 📋 TRADE HISTORY
    # =========================
    st.subheader("📋 Holdings")

    if st.session_state.portfolio:
        df_hold = pd.DataFrame([
            {"Stock": k, "Shares": v}
            for k, v in st.session_state.portfolio.items()
        ])
        st.dataframe(df_hold, use_container_width=True)

    # =========================
    # 📊 CHART
    # =========================
    st.subheader("📊 Chart")

    range_option = st.selectbox("Time Range", ["1W", "1M", "3M", "ALL"])

    fig = create_candlestick(df, stock, range_option)
    st.plotly_chart(fig, use_container_width=True, key=f"user_chart_{stock}_{range_option}")
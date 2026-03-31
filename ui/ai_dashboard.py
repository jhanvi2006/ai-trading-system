import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from utils.data_loader import load_clean_data
from utils.charts import create_candlestick
from utils.portfolio import calculate_portfolio_value

from src.genetic_algorithm import genetic_algorithm
from src.agent import TradingAgent
from src.simulator import simulate_trading


def show_ai_dashboard():

    stock = st.session_state.get('selected_stock', 'AAPL')
    df = load_clean_data(stock)
    prices = df['Close'].values

    # =========================
    # 🌍 MARKET OVERVIEW
    # =========================
    st.subheader("🌍 Live Market")

    cols = st.columns(5)
    stocks = ["AAPL", "AMZN", "GOOGL", "MSFT", "NVDA"]

    for i, s in enumerate(stocks):
        df_s = load_clean_data(s)
        change_pct = ((df_s['Close'].iloc[-1] / df_s['Close'].iloc[-2] - 1) * 100)

        with cols[i]:
            st.metric(s, f"${df_s['Close'].iloc[-1]:.2f}", f"{change_pct:+.1f}%")

    # =========================
    # 🔮 PREDICTION
    # =========================
    trend = "🔼 Bullish" if prices[-1] > prices[-2] else "🔽 Bearish"
    st.success(f"📊 AI Prediction: **{trend}**", icon="🔮")

    # =========================
    # 📈 CHART
    # =========================
    st.subheader("📈 Price Analysis")

    range_option = st.selectbox("View", ["1W", "1M", "3M", "ALL"])

    fig = create_candlestick(df, stock, range_option)
    st.plotly_chart(fig, use_container_width=True, key=f"ai_chart_{stock}_{range_option}")

    # =========================
    # 🚀 RUN AI
    # =========================
    if st.button("🚀 Optimize & Run AI Trading", type="primary", use_container_width=True):

        progress = st.progress(0)
        status = st.empty()

        status.info("🎯 Running Genetic Algorithm...")
        progress.progress(30)
        best_params = genetic_algorithm(prices)

        status.info("🤖 Training RL Agent...")
        progress.progress(70)
        agent = TradingAgent(2, 3, best_params["lr"], best_params["gamma"], best_params["epsilon"])

        status.info("⚡ Simulating Trading...")
        progress.progress(100)

        final_value, trades, wins, total_trades, history = simulate_trading(agent, prices)

        progress.empty()
        st.success("✅ AI Trading Complete!")

        profit = final_value - 10000
        profit_pct = (profit / 10000) * 100

        # =========================
        # 📊 RESULTS
        # =========================
        st.subheader("🏆 Trading Results")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("💰 Final Value", f"${final_value:.2f}", f"{profit_pct:+.1f}%")
        col2.metric("📈 Profit", f"${profit:.2f}")
        col3.metric("⚡ Trades", total_trades)

        win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
        col4.metric("🥇 Win Rate", f"{win_rate:.1f}%")

        # =========================
        # 📈 PORTFOLIO GRAPH
        # =========================
        st.subheader("📈 Portfolio Growth")

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(y=history, mode='lines', name='Portfolio'))
        fig2.add_hline(y=10000, line_dash="dash", line_color="red")

        st.plotly_chart(fig2, use_container_width=True, key="ai_portfolio_chart")

        # =========================
        # 📜 TRADE HISTORY
        # =========================
        st.subheader("📜 Trade History")

        trades_df = pd.DataFrame(trades)

        if not trades_df.empty:
            st.dataframe(trades_df, use_container_width=True)

        # =========================
        # ⚖️ AI VS USER
        # =========================
        if "balance" in st.session_state:

            user_value = st.session_state.balance + calculate_portfolio_value(st.session_state.portfolio)

            st.subheader("⚖️ AI vs User")

            fig3 = go.Figure()
            fig3.add_bar(name="User", x=["Value"], y=[user_value])
            fig3.add_bar(name="AI", x=["Value"], y=[final_value])

            st.plotly_chart(fig3, use_container_width=True, key="ai_vs_user_chart")

        # =========================
        # 🔄 RESET
        # =========================
        if st.button("🔄 Reset Simulation"):
            st.rerun()
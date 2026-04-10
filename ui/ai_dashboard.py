import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from utils.data_loader import load_clean_data
from utils.charts import create_candlestick
from utils.portfolio import calculate_portfolio_value

from src.genetic_algorithm import genetic_algorithm
from src.simulator import simulate_trading_ga

@st.cache_data
def run_genetic_algorithm(_df):
    """Cached GA"""
    return genetic_algorithm(_df)

def show_ai_dashboard():
    stock = st.session_state.get('selected_stock', 'AAPL')
    df = load_clean_data(stock)
    prices = df['Close'].values

    # =========================
    # 🌍 MARKET OVERVIEW
    # =========================
    st.subheader("🌍 Live Market")

    # ⚡ PERF: Cache market data
    if "market_data" not in st.session_state:
        st.session_state.market_data = {s: load_clean_data(s) for s in ["AAPL", "AMZN", "GOOGL", "MSFT", "NVDA"]}
    
    cols = st.columns(5)
    stocks = ["AAPL", "AMZN", "GOOGL", "MSFT", "NVDA"]
    current_prices = {}

    for i, s in enumerate(stocks):
        df_s = st.session_state.market_data[s]
        current_price = df_s['Close'].iloc[-1]
        current_prices[s] = current_price
        if len(df_s) > 1:
            change_pct = ((current_price / df_s['Close'].iloc[-2] - 1) * 100)
        else:
            change_pct = 0

        with cols[i]:
            st.metric(s, f"${current_price:.2f}", f"{change_pct:+.1f}%")

    # =========================
    # 💡 GA PREDICTION (Basic)
    # =========================
    if "ga_strategy" in st.session_state:
        strat = st.session_state["ga_strategy"]
        last_price = df['Close'].iloc[-1]
        prev_price = df['Close'].iloc[-2]
        change = (last_price - prev_price) / prev_price
        
        if change < -strat.get("buy_threshold", 0.02):
            trend = "🔼 Bullish (GA Recommends: BUY)"
        elif change > strat.get("sell_threshold", 0.03):
            trend = "🔽 Bearish (GA Recommends: SELL)"
        else:
            trend = "➡️ Neutral (GA Recommends: HOLD)"
            
        st.success(f"🤖 Live Strategy Prediction: **{trend}**", icon="💡")
    else:
        st.info("💡 Click 'Optimize & Run Trading' below to generate strategy predictions!", icon="⚙️")

    # =========================
    # 📈 CHART
    # =========================
    st.subheader("📈 Price Analysis")

    range_option = st.selectbox("View", ["1W", "1M", "3M", "ALL"])

    fig = create_candlestick(df, stock, range_option)

    # =========================
    # ✅ ADD BUY/SELL MARKERS
    # =========================
    if "ai_trades" in st.session_state:
        trades = st.session_state["ai_trades"]

        buy_x, buy_y = [], []
        sell_x, sell_y = [], []

        df_view = df.copy()
        if range_option == "1W":
            df_view = df.tail(7)
        elif range_option == "1M":
            df_view = df.tail(30)
        elif range_option == "3M":
            df_view = df.tail(90)

        for t in trades:
            step = t["step"]
            if step not in df_view.index:
                continue

            date = df.loc[step, "Date"]
            price = t["price"]

            if t["type"] == "BUY":
                buy_x.append(date)
                buy_y.append(price)
            elif t["type"] == "SELL":
                sell_x.append(date)
                sell_y.append(price)

        # BUY markers
        fig.add_trace(go.Scatter(
            x=buy_x,
            y=buy_y,
            mode="markers",
            name="BUY",
            marker=dict(color="green", size=10, symbol="triangle-up")
        ))

        # SELL markers
        fig.add_trace(go.Scatter(
            x=sell_x,
            y=sell_y,
            mode="markers",
            name="SELL",
            marker=dict(color="red", size=10, symbol="triangle-down")
        ))

    st.plotly_chart(fig, use_container_width=True, key=f"ai_chart_{stock}_{range_option}")

    # =========================
    # 🚀 RUN OPTIMIZATION
    # =========================
    if st.button("⚙️ Optimize & Run Trading", type="primary", use_container_width=True):

        progress = st.progress(0)
        status = st.empty()

        # 🔹 GA
        status.info("🎯 Running Genetic Algorithm...")
        progress.progress(40)
        best_params = genetic_algorithm(df)
        st.session_state["ga_strategy"] = best_params

        # 🔹 FINAL RUN
        status.info("⚡ Simulating Trading...")
        progress.progress(80)

        result = simulate_trading_ga(best_params, df)

        # ✅ STORE TRADES
        st.session_state["ai_trades"] = result["trades"]

        progress.progress(100)
        status.empty()
        progress.empty()
        st.success("✅ Strategy Optimization and Trading Complete!")

        final_value = result["final_balance"]
        profit = result["profit"]
        profit_pct = (profit / 10000) * 100

        trades = result["trades"]
        total_trades = result["total_trades"]
        wins = result["wins"]
        history = result["history"]

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
        # 📈 PORTFOLIO
        # =========================
        st.subheader("📈 Portfolio Growth")

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(y=history, mode='lines', name='Portfolio'))
        fig2.add_hline(y=10000, line_dash="dash", line_color="red")

        st.plotly_chart(fig2, use_container_width=True)

        # =========================
        # 📜 TRADE HISTORY
        # =========================
        st.subheader("📜 Trade History")

        trades_df = pd.DataFrame(trades)

        if not trades_df.empty:
            st.dataframe(trades_df, use_container_width=True)

        # =========================
        # 🔄 RESET
        # =========================
        if st.button("🔄 Reset Simulation"):
            st.session_state.pop("ai_trades", None)
            st.session_state.pop("ga_strategy", None)
            if "market_data" in st.session_state:
                del st.session_state.market_data
            st.rerun()

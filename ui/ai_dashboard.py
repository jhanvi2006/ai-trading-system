import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from utils.data_loader import load_clean_data
from utils.charts import create_candlestick
from utils.portfolio import calculate_portfolio_value

from src.genetic_algorithm import genetic_algorithm
from src.rl_agent import RLTradingAgent
from src.simulator import simulate_trading_rl

@st.cache_data
def run_genetic_algorithm(_df):
    """Cached GA"""
    return genetic_algorithm(_df)

@st.cache_data
def train_rl_agent(_train_df, _strategy):
    """Cached RL training"""
    agent = RLTradingAgent(actions=["BUY", "SELL", "HOLD"])
    agent.set_initial_strategy(_strategy)
    for _ in range(25):  # Reduced episodes
        simulate_trading_rl(agent, _train_df)
    return agent

@st.cache_data
def final_simulation(_agent, _test_df):
    """Cached final sim"""
    return simulate_trading_rl(_agent, _test_df)


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
        change_pct = ((current_price / df_s['Close'].iloc[-2] - 1) * 100)

        with cols[i]:
            st.metric(s, f"${current_price:.2f}", f"{change_pct:+.1f}%")

    # =========================
    # 🔮 PREDICTION
    # =========================
    if "ai_agent" in st.session_state:
        trained_agent = st.session_state["ai_agent"]
        
        last_row = df.iloc[-1]
        prev_row = df.iloc[-2]
        current_state = trained_agent.get_state(last_row, prev_close=prev_row["Close"], prev_ma=prev_row["MA_10"])
        next_action = trained_agent.choose_action(current_state)
        
        if next_action == "BUY":
            trend = "🔼 Bullish (AI Recommends: BUY)"
        elif next_action == "SELL":
            trend = "🔽 Bearish (AI Recommends: SELL)"
        else:
            trend = "➡️ Neutral (AI Recommends: HOLD)"
            
        st.success(f"🤖 Live AI Prediction: **{trend}**", icon="🔮")
    else:
        st.info("💡 Click 'Optimize & Run AI Trading' below to generate real-time RL predictions!", icon="🔮")

    # =========================
    # 📈 CHART
    # =========================
    st.subheader("📈 Price Analysis")

    range_option = st.selectbox("View", ["1W", "1M", "3M", "ALL"])

    fig = create_candlestick(df, stock, range_option)

    # =========================
    # ✅ ADD BUY/SELL MARKERS (FINAL FIX)
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
    # ⚙️ GA CONFIGURATION
    # =========================
    st.subheader("⚙️ AI Initialization Settings")
    colA, colB = st.columns(2)
    sel_type = colA.selectbox("Selection Method", ["Tournament", "Roulette Wheel"])
    cross_type = colB.selectbox("Crossover Method", ["Uniform", "Single-Point"])

    # =========================
    # 🚀 RUN AI
    # =========================
    if st.button("🚀 Optimize & Run AI Trading", type="primary", use_container_width=True):

        progress = st.progress(0)
        status = st.empty()

        # 🔹 GA
        status.info("🎯 Running Genetic Algorithm...")
        progress.progress(30)
        ga_result = genetic_algorithm(df, selection_type=sel_type, crossover_type=cross_type)
        best_params = ga_result["best_params"]
        st.session_state["ga_history"] = ga_result["history"]

        # 🔹 RL INIT
        status.info("🤖 Initializing RL Agent with GA...")
        progress.progress(70)

        agent = RLTradingAgent(actions=["BUY", "SELL", "HOLD"])

        ga_strategy = {
            "buy_threshold": best_params.get("buy_threshold", 0.02),
            "sell_threshold": best_params.get("sell_threshold", 0.03),
            "position_size_pct": best_params.get("position_size_pct", 0.1)
        }

        agent.set_initial_strategy(ga_strategy)


        # Train/test split to prevent overfitting
        split = int(len(df) * 0.8)
        train_df = df.iloc[:split]
        test_df = df.iloc[split:]

        # 🔹 TRAIN RL on train
        status.info("🧠 Training RL Agent...")
        for _ in range(50):
            simulate_trading_rl(agent, train_df)

        # 🔹 FINAL RUN on test
        status.info("⚡ Simulating Trading...")
        progress.progress(100)

        result = simulate_trading_rl(agent, test_df)


        # ✅ STORE TRADES & AGENT
        st.session_state["ai_trades"] = result["trades"]
        st.session_state["ai_agent"] = agent

        progress.empty()
        st.success("✅ AI Trading Complete!")

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
        # 🧬 GA & 🤖 RL INSIGHTS PANELS
        # =========================
        st.subheader("🧠 Under The Hood: AI Training Insights")

        with st.expander("🧬 Genetic Algorithm Evolution (Step-by-Step)"):
            st.write(f"The Genetic Algorithm evaluates simulated trading strategies, selecting the best via **{sel_type} Selection**, breeding them via **{cross_type} Crossover**, and applying random **Mutations**.")
            
            ga_history = st.session_state.get("ga_history", [])
            if ga_history:
                st.markdown("### 📈 Convergence Graph")
                gens = [h["generation"] for h in ga_history]
                top_fits = [h["best_fitness"] for h in ga_history]
                avg_fits = [h["average_fitness"] for h in ga_history]
                
                fig_ga = go.Figure()
                fig_ga.add_trace(go.Scatter(x=gens, y=top_fits, mode='lines+markers', name='Top Fitness'))
                fig_ga.add_trace(go.Scatter(x=gens, y=avg_fits, mode='lines+markers', name='Avg Fitness'))
                fig_ga.update_layout(xaxis_title="Generation", yaxis_title="Fitness Score", margin=dict(l=0, r=0, t=10, b=0))
                st.plotly_chart(fig_ga, use_container_width=True)

                st.divider()

                gen_idx = st.slider("Select Generation to View:", 1, len(ga_history), 1) - 1
                gen_data = ga_history[gen_idx]
                
                st.markdown(f"### Generation {gen_data['generation']}")
                c1, c2 = st.columns(2)
                c1.metric("Top Fitness (Score)", f"{gen_data['best_fitness']:.1f}")
                c2.metric("Avg Fitness", f"{gen_data['average_fitness']:.1f}")
                
                if "elites_count" in gen_data:
                    st.info(f"🏆 **Elitism:** The top {gen_data['elites_count']} individuals were carried over untouched to this generation.", icon="🛡️")

                st.markdown("**Top Individuals:**")
                st.json(gen_data["top_individuals"])
                
                st.markdown("**Breeding Operations (Sample):**")
                # Show first 3 operations to not overload the UI
                for idx, op in enumerate(gen_data["operations"][:3]):
                    st.markdown(f"#### Child {idx+1}")
                    st.write(f"🧬 **Parent 1:** {op['parent1']}")
                    st.write(f"🧬 **Parent 2:** {op['parent2']}")
                    st.write(f"✨ **Resulting Child (after Crossover & Mutation):** {op['child']}")
                    if op['mutations']:
                        st.warning(f"Mutations Applied on: {', '.join(op['mutations'])}")
                    st.divider()

        with st.expander("🤖 Reinforcement Learning Q-Learning Summary"):
            st.write("The RL Agent learns optimal actions over time using the **Q-Learning** algorithm.")
            st.markdown(
                """
                - **State Space**: `(MA Slope, RSI Zone, Price Zone, Volatility Zone)`
                - **Action Space**: `[BUY, SELL, HOLD]`
                - **Reward Structure**: Positive for profit-taking, negative/zero for inactivity and losses.
                """
            )
                
            if "ai_agent" in st.session_state:
                st.markdown("**Top Learned Q-Values (State-Action Pairs):**")
                q_table = st.session_state["ai_agent"].q_table
                
                # Sort descending by Q-value to show strongest learned rules
                sorted_q = sorted(q_table.items(), key=lambda x: x[1], reverse=True)[:10]
                q_df = pd.DataFrame([
                    {"State": str(state), "Action": action, "Q-Value": round(val, 3)} 
                    for (state, action), val in sorted_q
                ])
                st.dataframe(q_df, use_container_width=True)

        # =========================
        # ⚖️ AI VS USER
        # =========================
        if "balance" in st.session_state:

            user_value = st.session_state.balance + calculate_portfolio_value(st.session_state.portfolio, current_prices)

            st.subheader("⚖️ AI vs User")

            fig3 = go.Figure()
            fig3.add_bar(name="User", x=["Value"], y=[user_value])
            fig3.add_bar(name="AI", x=["Value"], y=[final_value])

            st.plotly_chart(fig3, use_container_width=True)

        # =========================
        # 🔄 RESET
        # =========================
        if st.button("🔄 Reset Simulation"):
            st.session_state.pop("ai_trades", None)
            st.session_state.pop("ai_agent", None)
            if "market_data" in st.session_state:
                del st.session_state.market_data
            st.rerun()

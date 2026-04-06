# 🚀 AI Trading System (GA + RL)

Welcome to the AI Trading System, a robust stock trading platform that leverages artificial intelligence to execute intelligent trades.

## 🌟 Review-3 Improvements & Core Features

### 1️⃣ Integration of Reinforcement Learning (Core AI Upgrade)
- Implemented a tabular Q-learning based trading agent.
- Agent learns optimal actions: **BUY** / **SELL** / **HOLD**.
- Uses an ε-greedy policy for balancing exploration vs exploitation.
- Q-table updated using Learning rate (α) and Discount factor (γ).
- Real-time learning during the trading simulation.

### 2️⃣ Advanced State Representation
Designed a multi-factor market state for the agent using:
- **Moving Average trend:** MA slope (UP / DOWN).
- **RSI zones:** Oversold / Neutral / Overbought.
- **Price movement zones:** High / Low / Neutral.
- **Volatility levels:** High / Medium / Low.
- *Enables deep, context-aware decision making for the AI.*

### 3️⃣ Genetic Algorithm + RL Hybrid Model
Integrated a Genetic Algorithm (GA) for pipeline optimization:
- Initial strategy configuration and parameter tuning (buy/sell thresholds, position sizing).
- The output from the GA is used to smartly initialize the RL Agent's Q-table.
- Greatly improves the convergence speed and baseline accuracy of the RL agent.

### 4️⃣ Realistic Trading Simulation Engine
A comprehensive trading simulator featuring:
- Dynamic balance tracking with handling of fractional/whole shares.
- Transaction cost modeling.
- Position sizing (risk-based trading).
- Calculation of active profit/loss, trade history logging, and tracking the baseline win rate.

### 5️⃣ Reward Engineering (Key AI Component)
Designed a custom reward function tailored for market success:
- Based off real portfolio value changes.
- Highly encourages profitable trades.
- Penalyzes inactivity (opportunity cost) to ensure learning aligns closely with realistic financial objectives.

### 6️⃣ Train-Test Split (Avoid Overfitting)
Dataset split into:
- **Training data:** 80% (RL agent trains safely on historical trends here).
- **Testing data:** 20% (Final evaluation performed effectively on unseen data to test live-market readiness).

### 7️⃣ Interactive AI Dashboard (Streamlit)
Developed a full, responsive UI using Streamlit:
- Live stock market overview displaying leading tickers.
- AI prediction displays (Bullish/Bearish indications).
- Advanced candlestick chart interactive visualizations.
- Features Buy/Sell markers directly drawn onto charts.
- Tracks portfolio growth dynamically in charting.

### 8️⃣ Performance Metrics & Evaluation
Displayed key trading metrics visually on the dashboard:
- Final portfolio total value and gross profit.
- Number of trades made natively by the AI.
- Win rate efficiency (%).
- Features a custom **AI vs User** comparison module to see who can trade better.

### 9️⃣ Optimization & Performance Improvements
Refined computation speed for UX scaling:
- Limiting training iterations properly using caching.
- Optimized datasets to ensure lightning-fast real-time usability on the web app.

### 🔟 System Completeness for Review-3
**End-to-End Pipeline Implemented:**
`Data Gathering → GA Optimization → RL Training → Run Simulation → Dashboard Visualization`

Fully functional AI-based trading system with zero "dummy" logic. All decisions are rigorously driven by the mathematical learning agent!

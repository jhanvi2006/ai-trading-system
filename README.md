# 🚀 AI Trading System (GA Optimization)

Welcome to the AI Trading System, a sophisticated stock trading simulator that leverages a Genetic Algorithm (GA) to automatically discover the most profitable trading rules. Designed for the AI Review 2.

## 🌟 Core Features

### 1️⃣ Genetic Algorithm Optimization
- Replaces static, hardcoded rules with evolutionary parameter tuning.
- System dynamically learns the optimal **Buy Threshold**, **Sell Threshold**, and **Position Sizing**.
- Evaluates generations of strategies based on a custom fitness function utilizing total return and Sharpe ratio heuristics.

### 2️⃣ Advanced Trading Simulation Engine
- Tracks an ongoing mock balance across stock market historical datasets.
- Includes dynamic allocation based on optimal percentage sizing (e.g. trade 10% or 20% of your account per position).
- Evaluates active profit and loss, win rate, and total trades efficiently.
- Handles fractional buys naturally.

### 3️⃣ Interactive AI Dashboard (Streamlit)
- Fully responsive user interface built using Streamlit.
- Features a **Live Market Overview** tracking the Top 5 Big Tech companies (AAPL, AMZN, GOOGL, MSFT, NVDA).
- High-fidelity **Candlestick Charting** with interactive timelines (1W, 1M, 3M, ALL).
- Plots computed **Buy & Sell Markers** directly on the chart so trading decision paths are transparent and visually verifiable.

### 4️⃣ Strategy Health Metrics
- Generates key performance indicators (KPIs) exactly like a real hedge fund dashboard:
  - Final Capital Value and Total Profit %
  - Execution count (Total Trades)
  - Quantitative Win Rate
  - Dynamic Portfolio Growth charting to visualize compounded capital over time.

### 5️⃣ System Completeness
**End-to-End Pipeline Implemented:**
`Data Gathering → Genetic Algorithm Optimization → Parameter Extraction → Full Dataset Simulation → Dashboard Visualization`

Fully functional trading simulator tuned strictly via mathematical evolutionary optimization!

## 🔧 Installation & Running
1. `pip install -r requirements.txt`
2. `streamlit run streamlit_app.py`

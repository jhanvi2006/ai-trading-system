def simulate_trading_rl(agent, data, initial_balance=10000):
    balance = initial_balance
    shares = 0.0  # float for fractional possible

    trades = []
    total_trades = 0
    wins = 0

    history = [initial_balance]

    transaction_cost_rate = 0.001
    position_size_pct = 0.1  # 10% risk per trade

    buy_trades = []  # Track open buys for proper P&L

    for i in range(1, len(data)):
        row = data.iloc[i]
        prev_row = data.iloc[i - 1]

        price = row["Close"]

        p_close = data.iloc[i-2]["Close"] if i > 1 else prev_row["Close"]
        p_ma = data.iloc[i-2]["MA_10"] if i > 1 else prev_row["MA_10"]
        state = agent.get_state(prev_row, prev_close=p_close, prev_ma=p_ma)

        action = agent.choose_action(state)

        old_value = balance + shares * prev_row["Close"]
        trade_made = False

        shares_to_trade = max(1, int((balance * position_size_pct) / price))
        shares_to_trade = min(shares_to_trade, int(shares)) if shares > 0 else shares_to_trade

        # BUY
        if action == "BUY" and balance >= price * shares_to_trade:
            cost = price * shares_to_trade * transaction_cost_rate
            shares += shares_to_trade
            balance -= (price * shares_to_trade + cost)

            trade_made = True
            buy_trades.append({"shares": shares_to_trade, "buy_price": price})

            trades.append({
                "type": "BUY",
                "price": price,
                "shares": shares_to_trade,
                "step": row.name
            })

        # SELL
        elif action == "SELL" and shares >= shares_to_trade:
            cost = price * shares_to_trade * transaction_cost_rate
            shares -= shares_to_trade
            balance += (price * shares_to_trade - cost)

            trade_made = True
            total_trades += 1

            # P&L for this sell
            sell_profit = (price - buy_trades[-1]["buy_price"]) * shares_to_trade if buy_trades else 0
            if sell_profit > 0:
                wins += 1
            if buy_trades:
                buy_trades.pop()  # Close last buy

            trades.append({
                "type": "SELL",
                "price": price,
                "shares": shares_to_trade,
                "step": row.name
            })

        # =========================
        # NEW VALUE
        # =========================
        new_value = balance + shares * price

        # REWARD: normalized profit + inactivity/sharpe penalty
        profit_pct = (new_value - old_value) / old_value
        if trade_made:
            reward = profit_pct * 10  # Scale
        else:
            reward = -0.1 * profit_pct  # Small opportunity cost

        next_state = agent.get_state(row, prev_close=prev_row["Close"], prev_ma=prev_row["MA_10"])
        agent.learn(state, action, reward, next_state)

        # Epsilon decay slower (every 10 steps equiv)
        if i % 10 == 0:
            agent.epsilon = max(0.01, agent.epsilon * 0.995)

        history.append(new_value)

    final_value = balance + shares * data.iloc[-1]["Close"]

    return {
        "final_balance": final_value,
        "profit": final_value - initial_balance,
        "trades": trades,
        "total_trades": total_trades,
        "wins": wins,
        "history": history
    }

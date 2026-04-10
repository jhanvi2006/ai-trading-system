def simulate_trading_ga(strategy, data, initial_balance=10000):
    balance = initial_balance
    shares = 0.0

    trades = []
    total_trades = 0
    wins = 0

    history = [initial_balance]

    # Use GA strategy parameters
    buy_threshold = strategy.get("buy_threshold", 0.02)
    sell_threshold = strategy.get("sell_threshold", 0.03)
    position_size_pct = strategy.get("position_size_pct", 0.1)

    buy_trades = []  # Track open buys for P&L tracking
    prices = data["Close"].values

    for i in range(1, len(prices)):
        price = prices[i]
        prev_price = prices[i - 1]
        
        change = (price - prev_price) / prev_price
        
        old_value = balance + shares * prev_price
        
        shares_to_trade = max(1, int((balance * position_size_pct) / price))
        shares_to_trade = min(shares_to_trade, int(shares)) if shares > 0 else shares_to_trade

        # BUY Logic: If price drops more than the threshold
        if change < -buy_threshold and balance >= price * shares_to_trade:
            shares += shares_to_trade
            balance -= price * shares_to_trade
            
            buy_trades.append({"shares": shares_to_trade, "buy_price": price})
            trades.append({
                "type": "BUY",
                "price": price,
                "shares": shares_to_trade,
                "step": data.index[i]
            })

        # SELL Logic: If price increases more than the threshold
        elif change > sell_threshold and shares >= shares_to_trade:
            shares -= shares_to_trade
            balance += price * shares_to_trade

            total_trades += 1

            # Check if this trade was profitable
            if buy_trades:
                sell_profit = (price - buy_trades[-1]["buy_price"]) * shares_to_trade
                if sell_profit > 0:
                    wins += 1
                buy_trades.pop()  # Close the latest active buy position

            trades.append({
                "type": "SELL",
                "price": price,
                "shares": shares_to_trade,
                "step": data.index[i]
            })

        new_value = balance + shares * price
        history.append(new_value)

    final_value = balance + shares * prices[-1]

    return {
        "final_balance": final_value,
        "profit": final_value - initial_balance,
        "trades": trades,
        "total_trades": total_trades,
        "wins": wins,
        "history": history
    }

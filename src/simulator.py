def simulate_trading(agent, prices):

    balance = 10000
    stock = 0

    trades = []
    portfolio_history = []

    wins = 0
    total_trades = 0

    for t in range(1, len(prices)-1):

        state = [prices[t], prices[t] - prices[t-1]]
        next_state = [prices[t+1], prices[t+1] - prices[t]]

        action = agent.choose_action(state)

        # BUY
        if action == 0 and balance >= prices[t]:
            stock += 1
            balance -= prices[t]

            trades.append({
                "type": "BUY",
                "price": prices[t],
                "day": t
            })

        # SELL
        elif action == 1 and stock > 0:
            stock -= 1
            balance += prices[t]

            trades.append({
                "type": "SELL",
                "price": prices[t],
                "day": t
            })

            if prices[t] > prices[t-1]:
                wins += 1

            total_trades += 1

        reward = (prices[t+1] - prices[t]) * stock
        agent.update(state, action, reward, next_state)

        portfolio_value = balance + stock * prices[t]
        portfolio_history.append(portfolio_value)

    final_value = balance + stock * prices[-1]

    return final_value, trades, wins, total_trades, portfolio_history
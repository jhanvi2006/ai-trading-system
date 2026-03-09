def teaching_agent(data, trades):

    feedback = []

    if len(data) < 10:
        return feedback

    open_price = data["Open"].iloc[-1]
    close_price = data["Close"].iloc[-1]
    high_price = data["High"].iloc[-1]
    low_price = data["Low"].iloc[-1]

    volatility = high_price - low_price

    # -------- MARKET ANALYSIS --------

    if close_price > open_price:
        feedback.append("Market insight: Bullish candle today — buyers dominated.")

    else:
        feedback.append("Market insight: Bearish candle today — sellers dominated.")

    if volatility > 5:
        feedback.append("Market insight: High volatility detected today.")

    # -------- TREND DETECTION --------

    recent_prices = data["Close"].iloc[-5:]

    if recent_prices.iloc[-1] > recent_prices.iloc[0]:
        trend = "uptrend"
        feedback.append("Trend insight: Market is currently in an uptrend.")

    else:
        trend = "downtrend"
        feedback.append("Trend insight: Market is currently in a downtrend.")

    # -------- USER BEHAVIOR ANALYSIS --------

    if len(trades) > 0:

        last_trade = trades[-1]

        trade_type = last_trade["Type"]
        trade_price = last_trade["Price"]

        # GOOD ENTRY DETECTION
        if trade_type == "Buy":

            if trend == "uptrend":
                feedback.append("Trading insight: Good entry — you bought during an upward trend.")

            else:
                feedback.append("Trading insight: Risky entry — buying during a downtrend can be dangerous.")

        # PANIC SELL DETECTION
        if trade_type == "Sell":

            if trend == "uptrend" and close_price > trade_price:
                feedback.append("Behavior insight: You sold early while the price continued rising.")

            if trend == "downtrend":
                feedback.append("Trading insight: Good sell — market is declining.")

    # -------- OVERTRADING DETECTION --------

    if len(trades) >= 5:
        feedback.append("Behavior insight: You are trading frequently. Avoid overtrading.")

    # -------- RANDOM TRADING DETECTION --------

    if len(trades) >= 4:

        buy_count = sum(1 for t in trades if t["Type"] == "Buy")
        sell_count = sum(1 for t in trades if t["Type"] == "Sell")

        if abs(buy_count - sell_count) <= 1:
            feedback.append("Behavior insight: Your trades appear random. Try following market trends.")

    return feedback
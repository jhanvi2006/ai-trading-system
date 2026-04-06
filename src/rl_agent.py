import numpy as np
import random


class RLTradingAgent:
    def __init__(self, actions, alpha=0.1, gamma=0.9, epsilon=0.2):
        self.actions = actions              # ["BUY", "SELL", "HOLD"]
        self.alpha = alpha                  # learning rate
        self.gamma = gamma                  # discount factor
        self.epsilon = epsilon              # exploration rate
        self.q_table = {}

    # =========================
    # STATE REPRESENTATION
    # =========================
    def get_state(self, row, prev_close=None, prev_ma=None):
        price = row["Close"]
        ma = row["MA_10"]
        rsi = row["RSI"]
        
        if prev_close is None:
            prev_close = row.get("prev_close", price)
            
        if prev_ma is None:
            prev_ma = row.get("prev_ma", ma)

        ma_slope = "UP" if ma > prev_ma else "DOWN"
        trend = "UP" if price > ma else "DOWN"

        # Price change %
        price_change = (price - prev_close) / prev_close
        if price_change > 0.02:
            price_zone = "HIGH"
        elif price_change < -0.02:
            price_zone = "LOW"
        else:
            price_zone = "NEUTRAL"

        # Volatility (std last 10 closes if available, else proxy)
        vol_proxy = abs(price_change) * 100
        if vol_proxy > 3:
            vol_zone = "HIGH"
        elif vol_proxy < 1:
            vol_zone = "LOW"
        else:
            vol_zone = "MED"

        # RSI zones
        if rsi < 30:
            rsi_zone = "OVERSOLD"
        elif rsi > 70:
            rsi_zone = "OVERBOUGHT"
        else:
            rsi_zone = "NEUTRAL"

        return (ma_slope, rsi_zone, price_zone, vol_zone)

    # =========================
    # Q-TABLE ACCESS
    # =========================
    def get_q(self, state, action):
        return self.q_table.get((state, action), 0.0)

    # =========================
    # ACTION SELECTION
    # =========================
    def choose_action(self, state):
        # Exploration vs Exploitation
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self.actions)

        q_values = [self.get_q(state, a) for a in self.actions]
        return self.actions[np.argmax(q_values)]

    # =========================
    # LEARNING (Q-LEARNING)
    # =========================
    def learn(self, state, action, reward, next_state):
        current_q = self.get_q(state, action)
        max_next_q = max([self.get_q(next_state, a) for a in self.actions])

        new_q = current_q + self.alpha * (
            reward + self.gamma * max_next_q - current_q
        )

        self.q_table[(state, action)] = new_q

    # =========================
    # GA → RL INITIALIZATION
    # =========================
    def set_initial_strategy(self, strategy):
        ma_slopes = ["UP", "DOWN"]
        rsi_states = ["OVERSOLD", "NEUTRAL", "OVERBOUGHT"]
        price_zones = ["HIGH", "LOW", "NEUTRAL"]
        vol_zones = ["HIGH", "MED", "LOW"]

        for ma_slope in ma_slopes:
            for rsi in rsi_states:
                for pz in price_zones:
                    for vz in vol_zones:
                        state = (ma_slope, rsi, pz, vz)

                        for action in self.actions:
                            # Strong BUY: Down slope, oversold, low price, low vol
                            if action == "BUY" and ma_slope == "DOWN" and rsi == "OVERSOLD" and pz == "LOW":
                                self.q_table[(state, action)] = strategy["buy_threshold"] * 10

                            # Strong SELL: Up slope, overbought, high price, high vol
                            elif action == "SELL" and ma_slope == "UP" and rsi == "OVERBOUGHT" and pz == "HIGH":
                                self.q_table[(state, action)] = strategy["sell_threshold"] * 10

                            # Defaults
                            else:
                                self.q_table[(state, action)] = 0.1

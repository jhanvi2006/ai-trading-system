import random
import numpy as np

def random_strategy():
    return {
        "buy_threshold": random.uniform(0.01, 0.05),
        "sell_threshold": random.uniform(0.01, 0.05),
        "position_size_pct": random.uniform(0.05, 0.2)
    }

def fitness(strategy, data):
    # ⚡ PERF: Sample 20% data for faster eval
    sample_size = max(100, len(data) // 5)
    sample_indices = np.random.choice(len(data), sample_size, replace=False)
    data_sample = data.iloc[sample_indices].reset_index(drop=True)
    
    balance = 10000.0
    shares = 0.0
    returns = []
    
    prices = data_sample["Close"].values
    for i in range(1, len(prices)):
        price = prices[i]
        prev_price = prices[i-1]
        
        change = (price - prev_price) / prev_price
        old_value = balance + shares * prev_price
        position_size = strategy.get("position_size_pct", 0.1)
        shares_to_trade = max(1, int((balance * position_size) / price))
        
        if change < -strategy["buy_threshold"] and balance > price * shares_to_trade:
            shares += shares_to_trade
            balance -= price * shares_to_trade
        elif change > strategy["sell_threshold"] and shares >= shares_to_trade:
            shares -= shares_to_trade
            balance += price * shares_to_trade
        
        new_value = balance + shares * price
        if old_value > 0:
            returns.append((new_value - old_value) / old_value)
    
    final_value = balance + shares * prices[-1]
    total_return = (final_value - 10000) / 10000
    import statistics
    sharpe = total_return / (statistics.stdev(returns) + 0.01) if len(returns) > 1 else 0
    
    return final_value + sharpe * 1000


def genetic_algorithm(data, population_size=20, generations=20):
    population = [random_strategy() for _ in range(population_size)]

    for gen in range(generations):
        # Fitness
        fitness_scores = [(strat, fitness(strat, data)) for strat in population]
        fitness_scores.sort(key=lambda x: x[1], reverse=True)
        population = [fs[0] for fs in fitness_scores]

        new_population = population[:10]  # Elitism: top 10

        while len(new_population) < population_size:
            # Tournament selection
            p1 = random.choice(population[:15])
            p2 = random.choice(population[:15])

            child = {
                "buy_threshold": random.uniform(p1["buy_threshold"], p2["buy_threshold"]),
                "sell_threshold": random.uniform(p1["sell_threshold"], p2["sell_threshold"]),
                "position_size_pct": (p1["position_size_pct"] + p2["position_size_pct"]) / 2
            }

            # Mutation
            if random.random() < 0.3:
                child["buy_threshold"] += random.uniform(-0.01, 0.01)
                child["buy_threshold"] = max(0.001, min(0.1, child["buy_threshold"]))
            if random.random() < 0.3:
                child["sell_threshold"] += random.uniform(-0.01, 0.01)
                child["sell_threshold"] = max(0.001, min(0.1, child["sell_threshold"]))
            if random.random() < 0.3:
                child["position_size_pct"] += random.uniform(-0.02, 0.02)
                child["position_size_pct"] = max(0.01, min(0.3, child["position_size_pct"]))

            new_population.append(child)

        population = new_population

    return population[0]

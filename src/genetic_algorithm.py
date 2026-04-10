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


def genetic_algorithm(data, population_size=20, generations=20, selection_type="Tournament", crossover_type="Uniform"):
    population = [random_strategy() for _ in range(population_size)]
    history = []

    for gen in range(generations):
        # Fitness
        fitness_scores = [(strat, fitness(strat, data)) for strat in population]
        fitness_scores.sort(key=lambda x: x[1], reverse=True)
        population = [fs[0] for fs in fitness_scores]

        elite_count = 10

        # Log History
        gen_info = {
            "generation": gen + 1,
            "best_fitness": fitness_scores[0][1],
            "average_fitness": sum(fs[1] for fs in fitness_scores) / len(fitness_scores),
            "top_individuals": [{"strategy": fs[0].copy(), "fitness": fs[1]} for fs in fitness_scores[:3]],
            "elites_count": elite_count,
            "operations": []
        }

        new_population = population[:elite_count]  # Elitism: top 10

        while len(new_population) < population_size:
            # Selection
            if selection_type == "Roulette Wheel":
                min_fit = min(f[1] for f in fitness_scores)
                offset = abs(min_fit) + 1 if min_fit <= 0 else 0
                total_fit = sum(f[1] + offset for f in fitness_scores)
                
                def pick_roulette():
                    pick = random.uniform(0, total_fit)
                    current = 0
                    for f in fitness_scores:
                        current += (f[1] + offset)
                        if current > pick:
                            return f[0]
                    return fitness_scores[-1][0]
                    
                p1 = pick_roulette()
                p2 = pick_roulette()
            else:
                # Tournament selection (default)
                p1 = random.choice(population[:15])
                p2 = random.choice(population[:15])

            # Crossover
            child = {}
            keys = ["buy_threshold", "sell_threshold", "position_size_pct"]
            
            if crossover_type == "Single-Point":
                split_idx = random.choice([1, 2])
                for i, key in enumerate(keys):
                    if i < split_idx:
                        child[key] = p1[key]
                    else:
                        child[key] = p2[key]
            else:
                # Textbook Uniform Crossover (default)
                for key in keys:
                    if random.random() < 0.5:
                        child[key] = p1[key]
                    else:
                        child[key] = p2[key]

            mutations = []
            # Mutation
            if random.random() < 0.3:
                child["buy_threshold"] += random.uniform(-0.01, 0.01)
                child["buy_threshold"] = max(0.001, min(0.1, child["buy_threshold"]))
                mutations.append("buy_threshold")
            if random.random() < 0.3:
                child["sell_threshold"] += random.uniform(-0.01, 0.01)
                child["sell_threshold"] = max(0.001, min(0.1, child["sell_threshold"]))
                mutations.append("sell_threshold")
            if random.random() < 0.3:
                child["position_size_pct"] += random.uniform(-0.02, 0.02)
                child["position_size_pct"] = max(0.01, min(0.3, child["position_size_pct"]))
                mutations.append("position_size_pct")
                
            gen_info["operations"].append({
                "parent1": p1.copy(),
                "parent2": p2.copy(),
                "child": child.copy(),
                "mutations": mutations
            })

            new_population.append(child)

        population = new_population
        history.append(gen_info)

    # Return structured dict containing best parameters and evolution tracking
    return {
        "best_params": population[0],
        "history": history
    }

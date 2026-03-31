import random
from .simulator import simulate_trading
from .agent import TradingAgent

def genetic_algorithm(prices):

    population = [
        {
            "lr": random.uniform(0.001, 0.1),
            "gamma": random.uniform(0.8, 0.99),
            "epsilon": random.uniform(0.01, 0.2)
        }
        for _ in range(5)
    ]

    best = None
    best_score = -float("inf")

    for individual in population:

        agent = TradingAgent(2, 3,
            individual["lr"],
            individual["gamma"],
            individual["epsilon"]
        )

        score, _, _, _, _ = simulate_trading(agent, prices)

        if score > best_score:
            best_score = score
            best = individual

    return best
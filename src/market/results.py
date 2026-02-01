def compute_market_results(market_state):
    results = {}

    price = market_state["clearing_price"]
    generation = market_state["generation"]

    for tech, gen in generation.items():
        cost = gen["price"] * gen["quantity"]
        revenue = price * gen["quantity"]

        results[tech] = {
            "generation": gen["quantity"],
            "revenue": revenue,
            "cost": cost,
            "profit": revenue - cost,
        }

    return results

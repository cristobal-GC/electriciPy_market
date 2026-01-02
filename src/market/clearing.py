def market_clearing(offers: dict, demand_quantity: float):
    """
    Calcula el precio de casación y la asignación de generación por tecnología.

    Parameters
    ----------
    offers : dict
        {"tecnología": {"price": float, "capacity": float}, ...}
    demand_quantity : float
        Demanda fija del mercado

    Returns
    -------
    clearing_price : float
        Precio de casación (marginal)
    generation : dict
        Generación asignada por tecnología
    """
    # Ordenar ofertas por precio ascendente
    sorted_offers = sorted(offers.items(), key=lambda x: x[1]["price"])

    remaining_demand = demand_quantity
    generation = {}
    clearing_price = 0

    for tech, data in sorted_offers:
        cap = data["capacity"]
        price = data["price"]
        gen = min(cap, remaining_demand)
        generation[tech] = gen
        remaining_demand -= gen
        if gen > 0:
            clearing_price = price  # último precio que entra parcialmente o completamente
        if remaining_demand <= 0:
            break

    return clearing_price, generation

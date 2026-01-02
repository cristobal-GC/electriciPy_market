def step_offer_curve_data(offers: dict):
    """Devuelve x, y de curva de oferta escalonada"""
    sorted_offers = sorted(offers.items(), key=lambda x: x[1]["price"])
    x_points = [0]
    y_points = [0]
    cum_capacity = 0
    for _, data in sorted_offers:
        cum_capacity += data["capacity"]
        x_points.append(cum_capacity)
        y_points.append(data["price"])
    return x_points, y_points


def step_demand_curve_data(demand: dict):
    """Devuelve x, y de curva de demanda escalonada"""
    sorted_demand = sorted(demand.items(), key=lambda x: x[1]["price"], reverse=True)
    x_points = [0]
    y_points = [sorted_demand[0][1]["price"]]
    cum_quantity = 0
    for _, data in sorted_demand:
        cum_quantity += data["quantity"]
        x_points.append(cum_quantity)
        y_points.append(data["price"])
    return x_points, y_points

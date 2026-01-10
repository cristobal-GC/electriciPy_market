def step_supply_curve_data(supply_bids_dict: dict):
    """Devuelve x, y de curva de oferta escalonada"""
    sorted_supply_bids = sorted(supply_bids_dict.items(), key=lambda x: x[1]["price"])
    x_points = [0]
    y_points = [0]
    cum_capacity = 0
    for _, data in sorted_supply_bids:
        cum_capacity += data["quantity"]
        x_points.append(cum_capacity)
        y_points.append(data["price"])
    return x_points, y_points


def step_demand_curve_data(demand_bids_dict: dict):
    """Devuelve x, y de curva de demanda escalonada"""
    sorted_demand_bids = sorted(demand_bids_dict.items(), key=lambda x: x[1]["price"], reverse=True)
    x_points = [0]
    y_points = [sorted_demand_bids[0][1]["price"]]
    cum_quantity = 0
    for _, data in sorted_demand_bids:
        cum_quantity += data["quantity"]
        x_points.append(cum_quantity)
        y_points.append(data["price"])
    return x_points, y_points

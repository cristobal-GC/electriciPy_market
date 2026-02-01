def build_supply_bids(technologies_dic, slider_values):
    """
    Construye diccionario de ofertas a partir de tecnologías y los valores
    de los sliders pasados en el mismo orden que technologies_dic.items().
    """
    supply = {}
    # slider_values viene como [q1, p1, q2, p2, ...]
    values_iter = iter(slider_values)

    for tech_id, tech_cfg in technologies_dic.items():
        quantity = next(values_iter)
        price = next(values_iter)
        supply[tech_id] = {
            "quantity": quantity,
            "price": price
        }

    return supply

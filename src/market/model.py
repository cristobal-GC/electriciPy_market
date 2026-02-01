
from src.plotting.data import step_supply_curve_data, step_demand_curve_data
import numpy as np


def compute_clearing_price(offer_x, offer_y, demand_x, demand_y):
    for px, py in zip(offer_x, offer_y):
        demand_at_px = np.interp(px, demand_x, demand_y)
        if py >= demand_at_px:
            return py
    return offer_y[-1]


def compute_generation_by_tech(supply_bids, clearing_price):
    """
    Calcula la generación de cada tecnología según el precio de casación.

    Parameters
    ----------
    supply_bids : dict
        Diccionario con claves = tecnologías y valores = dict con
        'quantity' y 'price'.
        Ejemplo:
        {
            "nuclear": {"quantity": 10, "price": 5},
            "gas": {"quantity": 20, "price": 50},
            ...
        }
    clearing_price : float
        Precio de casación del mercado.

    Returns
    -------
    generation : dict
        Diccionario con la generación real de cada tecnología.
    """
    generation = {}
    for tech, bid in supply_bids.items():
        # Si el precio de oferta <= precio de casación, genera toda su capacidad
        if bid["price"] <= clearing_price:
            generation[tech] = bid["quantity"]
        else:
            generation[tech] = 0
    return generation




def clear_market(supply_bids, demand_bids):
    """
    Devuelve un dict con:
    - curvas
    - precio de casación
    - generación por tecnología
    """
    offer_x, offer_y = step_supply_curve_data(supply_bids)
    demand_x, demand_y = step_demand_curve_data(demand_bids)

    clearing_price = compute_clearing_price(
        offer_x, offer_y, demand_x, demand_y
    )

    generation = compute_generation_by_tech(
        supply_bids,
        clearing_price
    )

    return {
        "offer_curve": (offer_x, offer_y),
        "demand_curve": (demand_x, demand_y),
        "clearing_price": clearing_price,
        "generation": generation,
    }

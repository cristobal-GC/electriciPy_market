import pandas as pd
import numpy as np

def clear_market(*, df_supply: pd.DataFrame, df_demand: pd.DataFrame):
    """
    Market clearing by discretizing supply and demand into 1 MWh units.

    Returns:
        clearing_price: price of the marginal accepted unit
        cleared_quantity: total matched quantity
        df_supply_cleared: same as df_supply + 'cleared_quantity' + 'clearing_price'
    """

    # --- Crear arrays de unidades de oferta ---
    supply_units = []
    supply_idx = []

    for idx, row in df_supply.iterrows():
        units = np.full(int(row['quantity']), row['price'], dtype=float)
        supply_units.append(units)
        supply_idx.extend([idx]*len(units))

    if len(supply_units) == 0:
        return None, 0.0, df_supply.assign(cleared_quantity=0.0, clearing_price=None)

    supply_units = np.concatenate(supply_units)
    supply_idx = np.array(supply_idx)

    # --- Crear arrays de unidades de demanda ---
    demand_units = []
    for _, row in df_demand.iterrows():
        units = np.full(int(row['quantity']), row['price'], dtype=float)
        demand_units.append(units)

    if len(demand_units) == 0:
        return None, 0.0, df_supply.assign(cleared_quantity=0.0, clearing_price=None)

    demand_units = np.concatenate(demand_units)

    # --- Ordenar oferta ascendente y demanda descendente ---
    supply_sorted_idx = np.argsort(supply_units)
    supply_units = supply_units[supply_sorted_idx]
    supply_idx = supply_idx[supply_sorted_idx]

    demand_units = np.sort(demand_units)[::-1]

    # --- Casamiento unidad a unidad ---
    n_units = min(len(supply_units), len(demand_units))
    cleared = 0
    clearing_price = None

    for k in range(n_units):
        if supply_units[k] <= demand_units[k]:
            cleared += 1
            clearing_price = supply_units[k]
        else:
            break

    if cleared == 0:
        return None, 0.0, df_supply.assign(cleared_quantity=0.0, clearing_price=None)

    # --- Crear columna cleared_quantity sumando por oferta original ---
    df_supply_cleared = df_supply.copy()
    df_supply_cleared['cleared_quantity'] = 0.0
    df_supply_cleared['clearing_price'] = clearing_price

    for idx in np.unique(supply_idx[:cleared]):
        df_supply_cleared.loc[idx, 'cleared_quantity'] = min(
            df_supply.loc[idx, 'quantity'],
            (supply_idx[:cleared] == idx).sum()
        )

    return clearing_price, cleared, df_supply_cleared

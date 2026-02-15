import pandas as pd
import numpy as np


def clear_market(*,
                 df_supply: pd.DataFrame,
                 df_demand: pd.DataFrame,
                 ):
    """
    Robust uniform-price market clearing.
    """

    EPS = 1e-9

    # -------------------------
    # 1. Prepare DataFrames
    # -------------------------

    supply = df_supply.copy()
    demand = df_demand.copy()

    # Force numeric types (critical for robustness)
    supply["price"] = pd.to_numeric(supply["price"], errors="coerce")
    supply["quantity"] = pd.to_numeric(supply["quantity"], errors="coerce")
    demand["price"] = pd.to_numeric(demand["price"], errors="coerce")
    demand["quantity"] = pd.to_numeric(demand["quantity"], errors="coerce")

    # Remove invalid rows
    supply = supply.dropna(subset=["price", "quantity"])
    demand = demand.dropna(subset=["price", "quantity"])

    # Remove zero or negative quantities (economically irrelevant)
    supply = supply[supply["quantity"] > EPS].copy()
    demand = demand[demand["quantity"] > EPS].copy()

    # Sort merit order
    supply = supply.sort_values("price").reset_index(drop=True)
    demand = demand.sort_values("price", ascending=False).reset_index(drop=True)

    # Tracking columns
    supply["remaining"] = supply["quantity"].astype(float)
    demand["remaining"] = demand["quantity"].astype(float)

    cleared_quantity = 0.0
    clearing_price = np.nan

    i = j = 0

    # -------------------------
    # 2. Matching loop
    # -------------------------

    while i < len(supply) and j < len(demand):

        supply_price = float(supply.loc[i, "price"])
        demand_price = float(demand.loc[j, "price"])

        # Stop if no economic intersection
        if supply_price - demand_price > EPS:
            break

        supply_remaining = float(supply.loc[i, "remaining"])
        demand_remaining = float(demand.loc[j, "remaining"])

        # Skip exhausted blocks
        if supply_remaining <= EPS:
            supply.loc[i, "remaining"] = 0.0
            i += 1
            continue

        if demand_remaining <= EPS:
            demand.loc[j, "remaining"] = 0.0
            j += 1
            continue

        # Matched quantity
        q = min(supply_remaining, demand_remaining)

        cleared_quantity += q
        clearing_price = supply_price

        supply.loc[i, "remaining"] -= q
        demand.loc[j, "remaining"] -= q

    # -------------------------
    # 3. No clearing case
    # -------------------------

    if cleared_quantity <= EPS:

        df_out = df_supply.copy()

        df_out["cleared_quantity"] = 0.0
        df_out["remaining"] = df_out["quantity"]
        df_out["clearing_price"] = np.nan
        df_out["market_incomes"] = 0.0

        return None, 0.0, df_out.set_index("technology")

    # -------------------------
    # 4. Final assignment
    # -------------------------

    df_supply_cleared = supply.copy()

    df_supply_cleared["cleared_quantity"] = (
        df_supply_cleared["quantity"] - df_supply_cleared["remaining"]
    ).astype(float)

    # Robust marginal mask
    mask_marginal = abs(df_supply_cleared["price"] - clearing_price) < EPS

    marginal_total = df_supply_cleared.loc[mask_marginal, "quantity"].sum()

    if marginal_total > EPS:

        quantity_before = df_supply_cleared.loc[
            df_supply_cleared["price"] < clearing_price,
            "cleared_quantity"
        ].sum()

        remaining_to_allocate = cleared_quantity - quantity_before

        share = remaining_to_allocate / marginal_total
        share = min(max(share, 0.0), 1.0)

        df_supply_cleared.loc[mask_marginal, "cleared_quantity"] = (
            df_supply_cleared.loc[mask_marginal, "quantity"] * share
        )

    # -------------------------
    # 5. Economic results
    # -------------------------

    df_supply_cleared["clearing_price"] = float(clearing_price)
    df_supply_cleared["market_incomes"] = (
        df_supply_cleared["cleared_quantity"] * clearing_price
    )

    return (
        float(clearing_price),
        float(cleared_quantity),
        df_supply_cleared.set_index("technology")
    )

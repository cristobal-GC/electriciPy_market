

import pandas as pd



def clear_market(
    *,
    df_supply: pd.DataFrame,
    df_demand: pd.DataFrame,
):
    """
    Market clearing with stepwise supply and demand curves.

    df_supply columns: ["technology", "price", "quantity"]
    df_demand columns: ["price", "quantity"]

    Returns:
        clearing_price (float)
        cleared_quantity (float)
        df_supply_cleared (with cleared_quantity column)

    Logic:

        1. Define candidate prices
          The clearing price can only be one of the prices that actually appear in the market:
          prices from the supply offers or prices from the demand bids.

        2. Evaluate supply and demand at each candidate price
           For each candidate price p:

            · compute total supplied quantity from offers with price ≤ p

            · compute total demanded quantity from bids with price ≥ p

        3. Select the clearing price
          The clearing price is the lowest price p for which total supply is greater than or equal to total demand.
        The cleared quantity is the minimum of supply and demand at that price.
    """

    # --- Unique candidate prices ---
    candidate_prices = sorted(
        set(df_supply["price"]).union(df_demand["price"])
    )

    clearing_price = None
    cleared_quantity = None

    # --- Find clearing price ---
    for p in candidate_prices:
        q_supply = df_supply.loc[df_supply["price"] <= p, "quantity"].sum()
        q_demand = df_demand.loc[df_demand["price"] >= p, "quantity"].sum()

        if q_supply >= q_demand:
            clearing_price = p
            cleared_quantity = min(q_supply, q_demand)
            break

    if clearing_price is None:
        # No intersection
        return None, 0.0, df_supply.assign(cleared_quantity=0.0)

    # --- Allocate cleared quantities on supply side ---
    df_supply_cleared = df_supply.sort_values("price").copy()
    df_supply_cleared["cleared_quantity"] = 0.0

    # Fully accepted offers
    mask_lower = df_supply_cleared["price"] < clearing_price
    df_supply_cleared.loc[mask_lower, "cleared_quantity"] = df_supply_cleared.loc[mask_lower, "quantity"]

    quantity_before = df_supply_cleared.loc[mask_lower, "quantity"].sum()
    remaining_quantity = cleared_quantity - quantity_before
    remaining_quantity = max(0.0, remaining_quantity)

    # Marginal offers
    mask_marginal = df_supply_cleared["price"] == clearing_price
    marginal_total = df_supply_cleared.loc[mask_marginal, "quantity"].sum()

    if marginal_total > 0:
        share = remaining_quantity / marginal_total
        share = min(1.0, share)

        df_supply_cleared.loc[mask_marginal, "cleared_quantity"] = (
            df_supply_cleared.loc[mask_marginal, "quantity"] * share
        )


    # Add column with clearing price
    df_supply_cleared["clearing_price"] = clearing_price

    return clearing_price, cleared_quantity, df_supply_cleared

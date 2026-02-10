import pandas as pd


def clear_market(*,
                 df_supply: pd.DataFrame,
                 df_demand: pd.DataFrame,
                 ):
    """
    Market clearing with stepwise supply and demand curves.

    - Handles multiple supply offers at the same price.
    - Prorates marginal offers if needed.
    - Supports zero-price offers.
    - Quantities can be fractional (float), no int64 issues.

    Inputs
    ----------

    df_supply : pd.DataFrame
        
         id || technology | price | quantity
         ---++------------+-------+----------
          0 || solar      | 30    | 100
          1 || wind       | 25    |  80
          2 || gas        | 90    | 200    
    
    
    df_demand : pd.DataFrame

         id || price | quantity
         ---++-------+----------
          0 || 30    | 100
          1 || 25    |  10
          2 ||  0    |   5

    Outputs
    -------

    clearing_price : float
        Price of the marginal accepted supply offer.
    
        
    cleared_quantity : float
        Total matched quantity.
    
        
    df_supply_cleared : pd.DataFrame
        
         technology || price | quantity | remaining | cleared_quantity | clearing_price | market_incomes
         -----------++-------+------------+---------+------------------+----------------+----------------
          solar     || 30    | 100      |    ...
          wind      || 25    |  80      |    ...
          gas       || 90    | 200      |    ...    
    

    """

    # --- Prepare DataFrames ---
    supply = df_supply.sort_values("price").reset_index(drop=True).copy()
    demand = df_demand.sort_values("price", ascending=False).reset_index(drop=True).copy()

    # Columns for tracking
    supply["remaining"] = supply["quantity"].astype(float)
    demand["remaining"] = demand["quantity"].astype(float)

    cleared_quantity = 0.0
    clearing_price = None

    i = j = 0

    # --- Step 1: match quantities MWh to MWh, determine marginal price
    while i < len(supply) and j < len(demand):
        if supply.loc[i, "price"] > demand.loc[j, "price"]:
            break  # no more matches

        # Amount matched in this step
        q = min(supply.loc[i, "remaining"], demand.loc[j, "remaining"])
        if q <= 0:
            break

        cleared_quantity += q
        clearing_price = supply.loc[i, "price"]

        # Reduce remaining quantities
        supply.loc[i, "remaining"] -= q
        demand.loc[j, "remaining"] -= q

        if supply.loc[i, "remaining"] == 0:
            i += 1
        if demand.loc[j, "remaining"] == 0:
            j += 1

    if cleared_quantity == 0:
        # No intersection
        return None, 0.0, df_supply.assign(
            cleared_quantity=0.0,
            clearing_price=None
        )

    # --- Step 2: final assign
    df_supply_cleared = supply.copy()
    # Initialise as float to avoid int64 errors
    df_supply_cleared["cleared_quantity"] = (df_supply_cleared["quantity"] - df_supply_cleared["remaining"]).astype(float)

    # Distribute proportionally among the marginal offers if there are several at the same price.
    mask_marginal = df_supply_cleared["price"] == clearing_price
    marginal_total = df_supply.loc[df_supply["price"] == clearing_price, "quantity"].sum()

    if marginal_total > 0:
        # Amount covered by cheaper offers
        quantity_before = df_supply_cleared.loc[df_supply_cleared["price"] < clearing_price, "cleared_quantity"].sum()
        remaining = cleared_quantity - quantity_before
        share = remaining / marginal_total
        share = min(1.0, share)

        df_supply_cleared.loc[mask_marginal, "cleared_quantity"] = (
            df_supply_cleared.loc[mask_marginal, "quantity"] * share
        )


    ##### Add clearing price column
    df_supply_cleared["clearing_price"] = clearing_price

    ##### Add market incomes column
    df_supply_cleared["market_incomes"] = df_supply_cleared['cleared_quantity']*clearing_price


    return clearing_price, cleared_quantity, df_supply_cleared.set_index("technology")

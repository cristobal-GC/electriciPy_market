
import pandas as pd
import random


def estimate_demand(demand_dic, demand_uncertainty):

    # Demand in df
    df_demand = pd.DataFrame(demand_dic).T

    # Sort in decreasing price values
    df_demand = df_demand.sort_values("price", ascending=False)

    # Remove offers at zero price or below
    df_demand = df_demand[df_demand["price"] > 0]

    # Estimate min, max and mean value
    min_demand = df_demand.iloc[0]["quantity"]
    max_demand = df_demand["quantity"].sum()
    mean_demand = 0.5*(min_demand+max_demand)

    # Get random expected demand
    expected_demand = random.gauss(mean_demand, demand_uncertainty * mean_demand)
    
    ### To keep the value within min and max values in any case    
    #expected_demand = max(min_demand, min(expected_demand, max_demand)) 


    return round(expected_demand,1)
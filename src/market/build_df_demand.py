
import pandas as pd


def build_df_demand(demand_dic) -> pd.DataFrame:

    df_demand = pd.DataFrame([
        {"price": d["price"], "quantity": d["quantity"]}
        for d in demand_dic.values()
    ])

    return df_demand
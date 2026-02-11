
import numpy as np
import pandas as pd

from src.market.compute_generated_energy import compute_generated_energy



def dispatch_table(*,
                   df_supply_cleared: pd.DataFrame,
                   technologies_dic: dict,
                   config_dic: dict,
                   hydro_reserves: float,
                   co2_price: float
):
    """
    Converts `df_supply_cleared` into a transposed format for Dash DataTables,
    displaying technologies as columns and variables (price, quantity, cleared_quantity, etc.) as rows.
    

    Inputs
    ----------

    df_supply_cleared : pd.DataFrame
        
         technology || price | quantity | remaining | cleared_quantity | clearing_price | market_incomes
         -----------++-------+------------+---------+------------------+----------------+----------------
          solar     || 30    | 100      |    ...
          wind      || 25    |  80      |    ...
          gas       || 90    | 200      |    ...    


    ...


    Outputs
    -------

    data : list[dict]
         List of dictionaries row by row, ready to use in dash.DataTable

    columns : list[dict]
        Columns definition for dash.DataTable
    """

  

    ##### Create df by selecting and renaming specific columns from df_supply_cleared
    df = (
        df_supply_cleared[
            ['quantity', 'price', 'cleared_quantity', 'clearing_price', 'market_incomes']
        ]
        .rename(
            columns={
                'quantity': 'Offered energy',
                'price': 'Offered price',
                'cleared_quantity': 'Sold energy',
                'clearing_price': 'Market price',
                'market_incomes': 'Market incomes',
            },
        )
    )



    ##### Add generated energy
    df["Generated energy"] = np.nan
    
    for tech in df.index:
        df.at[tech, "Generated energy"] = compute_generated_energy(tech=tech,
                                                                   technologies_dic=technologies_dic,
                                                                   df=df,
                                                                   hydro_reserves=hydro_reserves
                                                                   )



    ##### Add unitary variable costs
    df['Unitary variable costs'] = df.index.map(lambda x: technologies_dic[x]['unitary_cost'])


    ##### Add CO2 emissions
    df['CO2 emissions'] = (df.index.map(lambda x: technologies_dic[x]['unitary_CO2']) * df["Generated energy"]).round(2)


    ##### Add CO2 price
    df['CO2 price'] = co2_price


    ##### Add variable costs
    df['Variable costs'] = df['Generated energy']*df['Unitary variable costs'] * (-1) + df['CO2 emissions']*co2_price * (-1)


    ##### Add energy imbalance
    df['Energy imbalance'] = df['Generated energy'] - df['Sold energy']


    ##### Add penalty factor    
    penalty_factor = (1 + np.abs(df['Energy imbalance'].sum()) * config_dic['unitary_penalty_fraction'])
    df['Penalty factor'] =  penalty_factor.round(2)


    ##### Add penalty price    
    df['Penalty price'] =  (penalty_factor * df['Market price']).round(2)


    ##### Add penalty
    df['Penalty'] = (df['Penalty price'] * df['Energy imbalance'].abs() * (-1)).round(2)


    ##### Add incomes
    df['TOTAL INCOMES'] = (df['Market incomes'] + df['Variable costs'] + df['Penalty']).round(2)




    ##### Rename tecnhologies
    rename_techs = {
                    tech_key: tech_data["name"]
                    for tech_key, tech_data in technologies_dic.items()
    }

    df = df.rename(index=rename_techs)



    ##### Transpose
    df_dispatch = df.T




    ##### Prepare data for DataTable
    data = []
    for var in df_dispatch.index:
        row = {"Variable": var}             # primera columna: nombre de la variable
        row.update(df_dispatch.loc[var].to_dict())  # resto de columnas: valores por tecnología
        data.append(row)

    ##### Columnas para DataTable
    columns = [{"name": "", "id": "Variable"}]
    columns += [{"name": tech, "id": tech} for tech in df_dispatch.columns]

    return data, columns

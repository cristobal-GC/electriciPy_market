
import numpy as np
import pandas as pd

from src.market.compute_generated_energy import compute_generated_energy



def dispatch_table(*,
                   df_supply_cleared: pd.DataFrame,
                   technologies_dic: dict,
                   config_dic: dict
):
    """
    Convierte df_supply_cleared en formato transpuesto para Dash DataTable,
    mostrando tecnologías como columnas y variables (price, quantity, cleared_quantity, etc.) como filas.

    Parámetros
    ----------
    df_supply_cleared : pd.DataFrame
        DataFrame con columnas como 'technology', 'price', 'quantity', 'cleared_quantity', etc.
    rename_vars : dict, opcional
        Diccionario para renombrar las filas (índices de df transpuesto).
        Ejemplo: {'price': 'Precio (EUR/MWh)', 'quantity': 'Cantidad (MWh)'}

    Retorna
    -------
    data : list[dict]
        Lista de diccionarios fila a fila, lista para usar en dash.DataTable
    columns : list[dict]
        Definición de columnas para dash.DataTable
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
                                                                   df=df
                                                                   )


    ##### Add unitary variable costs
    df['Unitary variable costs'] = df.index.map(lambda x: technologies_dic[x]['unitary_cost'])



    ##### Add variable costs
    df['Variable costs'] = df['Generated energy']*df['Unitary variable costs'] * (-1)


    ##### Add energy imbalance
    df['Energy imbalance'] = df['Generated energy'] - df['Sold energy']


    ##### Add penalty factor    
    penalty_factor = (1 + np.abs(df['Energy imbalance'].sum()) * config_dic['unitary_penalty_fraction'])
    df['Penalty factor'] =  penalty_factor.round(2)


    ##### Add penalty price    
    df['Penalty price'] =  penalty_factor * df['Market price']


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

import pandas as pd

def prepare_dispatch_table(
    df_supply_cleared: pd.DataFrame,
    rename_vars: dict = None
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

    # Transponer: filas = variables, columnas = tecnologías
    df_dispatch = df_supply_cleared.set_index("technology").T

    # Preparar data para DataTable
    data = []
    for var in df_dispatch.index:
        row_name = rename_vars.get(var, var) if rename_vars else var
        row = {"Variable": row_name}             # primera columna: nombre de la variable
        row.update(df_dispatch.loc[var].to_dict())  # resto de columnas: valores por tecnología
        data.append(row)

    # Columnas para DataTable
    columns = [{"name": "Variable", "id": "Variable"}]
    columns += [{"name": tech, "id": tech} for tech in df_dispatch.columns]

    return data, columns


def build_results_table(results):
    """
    Convierte el diccionario de resultados de mercado en una lista de dicts
    lista para pasar a dash_table.DataTable.

    Parameters
    ----------
    results : dict
        Diccionario con claves de tecnologías, cada una conteniendo
        campos como 'generation', 'profit', 'revenue', 'cost', etc.

    Returns
    -------
    table_data : list of dict
        Lista de diccionarios con claves: 'tech', 'generation', 'profit', etc.
    """
    table_data = []

    for tech, res in results.items():
        row = {
            "tech": tech,
            "generation": res.get("generation", 0),
            "profit": res.get("profit", 0),
            "revenue": res.get("revenue", 0),
            "cost": res.get("cost", 0)
        }
        table_data.append(row)

    return table_data

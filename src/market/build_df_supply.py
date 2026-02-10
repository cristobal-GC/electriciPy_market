
import pandas as pd


def build_df_supply(inputs) -> pd.DataFrame:

    ##### OPTION 1
    # rows = []
    #
    # for input_item in inputs:
    #     slider_id = input_item["id"]
    #     value = input_item["value"]
    #     tech = slider_id["tech"]
    #     field = slider_id["field"]   # can be 'price' or 'quantity'

    #     ### Check if there is already a row for this technology
    #     row = next((r for r in rows if r["technology"] == tech), None)
    #     if row is None:
    #         # Crear nueva fila
    #         row = {"technology": tech, "price": None, "quantity": None}
    #         rows.append(row)

    #     ### Assign the value
    #     row[field] = value

    # # Convert to DataFrame
    # df_supply = pd.DataFrame(rows)

    ##### OPTION 2
    rows = {}

    for input_item in inputs:
        slider_id = input_item["id"]
        tech = slider_id["tech"]
        field = slider_id["field"]

        rows.setdefault(tech, {"technology": tech, "price": None, "quantity": None})
        rows[tech][field] = input_item["value"]

    df_supply = pd.DataFrame(rows.values())


    return df_supply
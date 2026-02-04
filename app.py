import pandas as pd
# import numpy as np

from dash import Dash, html, dcc, dash_table, ALL, Input, Output, ctx

from src.layout.technology_block import technology_block
from src.config.parameters import load_scenario
from src.plotting.plot_market_curves import plot_market_curves
from src.market.clear_market import clear_market




# =====================
# Load scenario
# =====================
scenario = load_scenario("base_case")

### Unwrap relevant scenario variables
technologies_dic = scenario["technologies"]
demand_dic = scenario["demand"]
config_dic = scenario["config"]





# =====================
# Launch app
# =====================
app = Dash(__name__)





# =====================
# App layout
# =====================
app.layout = html.Div(
    [
        ### Title
        html.H1(f'{scenario["name"]}'),


        ### Technology blocks
        html.Div(
            [
                technology_block(                    
                    tech_key=tech_key,
                    tech_dic=tech_value,
                    config_dic=config_dic
                )
                for tech_key, tech_value in technologies_dic.items()
            ],
            style={
                "display": "flex",
                "justify-content": "center",
                "flex-wrap": "wrap",
            }
        ),


        ### Plot curves
        dcc.Graph(id="market_curve"),
        
        


        # ### Table
        # dash_table.DataTable(
        #     id="results_table",
        #     columns=[
        #         {"name": "Tecnología", "id": "tech"},
        #         {"name": "Generación", "id": "generation"},
        #         {"name": "Ganancia", "id": "profit"},
        #         # etc según lo que devuelva build_results_table
        #     ],
        #     data=[],
        #     style_table={"width": "100%"},
        #     style_cell={"textAlign": "center"},
        # ),


        ##### Prueba de renderizado del df
        dash_table.DataTable(
            id="debug_df",
            page_size=10,
        )
    ],
    style={"width": "90%", "margin": "auto"}
)





# =====================
# App callback
# =====================
#
# Cada callback define unos inputs y unos outputs.
# Posteriormente se define una función (con nombre arbitrario) 
# Los outputs de esa función se conectan con los outpus que se declaran en el callback
# La función se ejecuta cada vez que cambian los inputs
# Tiene sentido tener varios callbacks si los inputs son distintos, pero aquí no es el caso necesariamente



##### Inputs
# Los valores de los sliders tienen id estructurados, 
# lo que permite capturarlos fácilmente ahora sin necesidad de ser estrictos con el orden

@app.callback(
    Output("market_curve", "figure"),
    Output("debug_df", "data"),         # monitorización de df
    Output("debug_df", "columns"),      # monitorización de df
    # Output("results_table", "data"),
    Input({"type": "tech-slider", "tech": ALL, "field": ALL}, "value"),    
)


def update_market(values): 
    
    #################### Put all the slider values in df_supply:
    #
    # id | technology | price | quantity
    # ---+------------+-------+----------
    #  0 | solar      | 30    | 100
    #  1 | wind       | 25    |  80
    #  2 | gas        | 90    | 200
    #
    inputs = ctx.inputs_list[0]
    rows = []

    for input_item in inputs:
        slider_id = input_item["id"]
        value = input_item["value"]
        tech = slider_id["tech"]
        field = slider_id["field"]  # 'price' o 'quantity'

        # Buscar si ya existe la fila para esta tecnología
        row = next((r for r in rows if r["technology"] == tech), None)
        if row is None:
            # Crear nueva fila
            row = {"technology": tech, "price": None, "quantity": None}
            rows.append(row)

        # Asignar el valor correcto
        row[field] = value

    # Convertir a DataFrame
    df_supply = pd.DataFrame(rows)



    #################### Put the demand info from scenario dic into df_demand:
    #
    # id | price | quantity
    # ---+------------+-------+----------
    #  0 | 30    | 100
    #  1 | 25    |  10
    #  2 |  0    |   5
    #
    df_demand = pd.DataFrame([
        {"price": d["price"], "quantity": d["quantity"]}
        for d in demand_dic.values()
    ])



    #################### Clear market
    clearing_price, cleared_quantity, df_supply_cleared = clear_market(df_supply=df_supply, df_demand=df_demand)


    

    #################### Make plot
    fig = plot_market_curves(df_supply=df_supply, df_demand=df_demand)


    #################### Preparar datos para DataTable de monitorización
    data = df_supply_cleared.to_dict("records")
    columns = [{"name": c, "id": c} for c in df_supply_cleared.columns]
    
    return fig, data, columns







# =====================
# App run
# =====================
if __name__ == "__main__":
    app.run(debug=True, port=8050)   ##### port by default, 8050






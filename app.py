
import pandas as pd

from dash import Dash, html, dcc, dash_table, Input, Output, ALL, ctx

from src.config.parameters import load_scenario
from src.layout.dispatch_table_format import dispatch_table_format
from src.layout.technology_block import technology_block
from src.market.clear_market import clear_market
from src.market.dispatch_table import dispatch_table
from src.plotting.plot_market_curves import plot_market_curves





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
        # =====================
        # Title
        # =====================
        html.Div(
            html.H1(f'{scenario["name"]}'),
            style={"textAlign": "left",
                   "marginBottom": "30px"}
        ),

        # =====================
        # Technology blocks
        # =====================
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
                "gap": "30px"  # horizontal and vertical space between blocks
            }
        ),

        # =====================
        # Graph + Table side by side
        # =====================
        html.Div(
            [
                # --- Plot ---
                html.Div(
                    dcc.Graph(id="market_curve"),
                    style={
                        "width": "40%",   # ancho del gráfico
                        #"flex": 1,
                        "marginRight": "10px"  # espacio entre gráfico y tabla
                    }
                ),

                # --- Table ---
                html.Div(
                    dash_table.DataTable(
                        id="df_outputs",
                        page_size=20,
                        style_cell={
                            'fontSize': 20,
                            'fontFamily': 'sans-serif',  # fuente clara y moderna
                            'textAlign': 'center',
                            'minWidth': '100px',
                            #'maxWidth': '150px',
                        },
                        style_header={
                            'backgroundColor': "#C4DAF1",
                            'fontWeight': 'bold',
                            'fontSize': 22,
                            'textAlign': 'center'
                        },
                         style_data_conditional=dispatch_table_format()
                    ),
                    style={
                        "width": "40%",   # Table width
                        #"flex": 2,
                    }
                ),
            ],
            style={
                "display": "flex",
                "justify-content": "center",
                "align-items": "center",
                "marginBottom": "30px"
            }
        ),
    ],
    style={"fontFamily": "sans-serif"}
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
    Output("df_outputs", "data"),
    Output("df_outputs", "columns"),
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
    #
    # Add columns 'remaining', 'cleared_quantity' and 'cleared_price'
    clearing_price, cleared_quantity, df_supply_cleared = clear_market(df_supply=df_supply, df_demand=df_demand)


    

    #################### Make plot
    fig = plot_market_curves(df_supply=df_supply,
                             df_demand=df_demand,
                             clearing_price=clearing_price,
                             cleared_quantity=cleared_quantity)





    #################### Preparar datos para DataTable de monitorización
    data, columns = dispatch_table(df_supply_cleared=df_supply_cleared.round(2),
                                   technologies_dic=technologies_dic,
                                   config_dic=config_dic)

    
    return fig, data, columns







# =====================
# App run
# =====================
if __name__ == "__main__":
    app.run(debug=True, port=8050)   ##### port by default, 8050






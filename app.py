
from dash import Dash, html, dcc, Input, Output, dash_table
import numpy as np

from src.components.technology_block import technology_block
from src.config.parameters import load_scenario
from src.market.builders import build_supply_bids
from src.market.model import compute_clearing_price
from src.market.model import clear_market
from src.market.model import compute_generation_by_tech
from src.market.results import compute_market_results
from src.plotting.data import step_supply_curve_data, step_demand_curve_data
from src.plotting.plot import plot_market_curve
from src.tables.summary import build_results_table




# =====================
# Load scenario
# =====================
scenario = load_scenario()

technologies_dic = scenario["technologies"]
demand_dic = scenario["demand"]




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
                    name=tech_value["name"],
                    technology=tech_key,
                    scenario=scenario,
                    icon=tech_value["icon"],
                    quantity_slider_id=f"{tech_key}_quantity",
                    price_slider_id=f"{tech_key}_price",
                )
                for tech_key, tech_value in technologies_dic.items()
            ],
            style={
                "display": "flex",
                "justify-content": "center",
                "flex-wrap": "wrap",
            }
        ),


        ### Plot and results
        dcc.Graph(id="market_curve"),
        html.Div(
            id="market_info",
            style={"margin-top": "20px", "font-weight": "bold"}
        ),


        ### Table
        dash_table.DataTable(
            id="results_table",
            columns=[
                {"name": "Tecnología", "id": "tech"},
                {"name": "Generación", "id": "generation"},
                {"name": "Ganancia", "id": "profit"},
                # etc según lo que devuelva build_results_table
            ],
            data=[],
            style_table={"width": "100%"},
            style_cell={"textAlign": "center"},
        ),
    ],
    style={"width": "90%", "margin": "auto"}
)





# =====================
# App callback
# =====================
#
# Cada callback define unos inputs y unos outputs. 
# Los outputs se conectan con los outpus que se declaran a continuación
# El nombre de esa función es arbitrario, para claridad humana
# La función se ejecuta cada vez que cambian los inputs
# Tiene sentido tener varios callbacks si los inputs son distintos, pero aquí no es el caso necesariamente


##### Inputs
# Genera lista:
#   [ 
#     Input("Nuclear_quantity", "value"),
#     Input("Nuclear_price", "value"),  
#     Input("solar_wind_quantity", "value"),  
#     Input("solar_wind_price", "value"),  
#     ...
#   ]
#

inputs = [
    Input(f"{tech_key}_{field}", "value")
    for tech_key in technologies_dic.keys()
    for field in ("quantity", "price")
]


@app.callback(
    Output("market_curve", "figure"),
    Output("results_table", "data"),
    *inputs
)


def update_market(*values):

    supply = build_supply_bids(technologies_dic, values)

    market_state = clear_market(supply, demand_dic)

    results = compute_market_results(market_state)

    fig = plot_market_curve(
        *market_state["offer_curve"],
        *market_state["demand_curve"],
        market_state["clearing_price"]
    )

    table_data = build_results_table(results)

    return fig, table_data




# =====================
# App run
# =====================
if __name__ == "__main__":
    app.run(debug=True)






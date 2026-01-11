from dash import Dash, html, dcc, Input, Output
from src.config.parameters import load_scenario
from src.plotting.data import step_supply_curve_data, step_demand_curve_data
from src.plotting.plot import plot_market_curve
from src.components.technology_block import technology_block
import numpy as np



# =====================
# Load scenario
# =====================
scenario = load_scenario()

##### Initial parameters
demand_bids_dict = scenario["demand"]


technologies = [
    {"name": "Nuclear", "id": "nuclear", "icon": "nuclear.png"},
    {"name": "Solar-Wind", "id": "solar_wind", "icon": "solar_wind.png"},
    {"name": "Coal", "id": "coal", "icon": "coal.png"},
    {"name": "Gas", "id": "gas", "icon": "gas.png"},
    {"name": "Hydro", "id": "hydro", "icon": "hydro.png"},
]



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
                    name=tech["name"],
                    technology=tech["id"],
                    scenario=scenario,
                    icon=tech["icon"],
                    quantity_slider_id=f"{tech['id']}_quantity",
                    price_slider_id=f"{tech['id']}_price",
                )
                for tech in technologies
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
    ],
    style={"width": "90%", "margin": "auto"},
),




# =====================
# App callback
# =====================
@app.callback(
    Output("market_curve", "figure"),
    Output("market_info", "children"),
    Input("nuclear_quantity", "value"),
    Input("nuclear_price", "value"),
    Input("solar_wind_quantity", "value"),
    Input("solar_wind_price", "value"),        
    Input("coal_quantity", "value"),
    Input("coal_price", "value"),
    Input("gas_quantity", "value"),
    Input("gas_price", "value"),
    Input("hydro_quantity", "value"),
    Input("hydro_price", "value"),

)

def update_market_curve(
    nuclear_quantity,
    nuclear_price,
    solar_wind_quantity,
    solar_wind_price,
    coal_quantity,
    coal_price,
    gas_quantity,
    gas_price,
    hydro_quantity,
    hydro_price, 

):
    # Supply bids
    supply_bids_dict = {
        "nuclear": {            
            "quantity": nuclear_quantity,
            "price": nuclear_price,
        },
        "solar_wind": {            
            "quantity": solar_wind_quantity,
            "price": solar_wind_price,
        },                
        "coal": {            
            "quantity": coal_quantity,
            "price": coal_price,
        },        
        "gas": {
            "quantity": gas_quantity,
            "price": gas_price,            
        },
        "hydro": {            
            "quantity": hydro_quantity,
            "price": hydro_price,
        },
    }

    # Supply and demand curves
    offer_x, offer_y = step_supply_curve_data(supply_bids_dict)
    demand_x, demand_y = step_demand_curve_data(demand_bids_dict)

    # Precio de casación (criterio simple)
    clearing_price = None
    for px, py in zip(offer_x, offer_y):
        demand_at_px = np.interp(px, demand_x, demand_y)
        if py >= demand_at_px:
            clearing_price = py
            break

    if clearing_price is None:
        clearing_price = offer_y[-1]

    fig = plot_market_curve(
        offer_x,
        offer_y,
        demand_x,
        demand_y,
        clearing_price,
    )

    info_text = f"Precio de casación aproximado: {clearing_price} €/MWh"

    return fig, info_text


if __name__ == "__main__":
    app.run(debug=True)

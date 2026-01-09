from dash import Dash, html, dcc, Input, Output
from src.config.parameters import load_scenario
from src.plotting.data import step_offer_curve_data, step_demand_curve_data
from src.plotting.plot import plot_market_curve
from src.components.technology_block import technology_block
import numpy as np

# =====================
# Cargar escenario
# =====================
scenario = load_scenario()

# Parámetros iniciales
initial_gas_price = scenario["technologies"]["gas"]["price"]
initial_gas_capacity = scenario["technologies"]["gas"]["capacity"]

initial_nuclear_price = scenario["technologies"]["nuclear"]["price"]
initial_nuclear_capacity = scenario["technologies"]["nuclear"]["capacity"]

demand_dict = scenario["demand"]

# =====================
# Crear app
# =====================
app = Dash(__name__)

app.layout = html.Div(
    [
        html.H1("Mercado eléctrico: oferta y demanda escalonada"),

        # ---------- Bloques de tecnologías ---------- (se ponen todos en línea, luego se ajustan en filas según la pantalla

        html.Div(
            [
                technology_block(
                    name="Gas",
                    icon="gas.png",
                    price_slider_id="gas_price",
                    quantity_slider_id="gas_quantity",
                    price=initial_gas_price,
                    quantity=initial_gas_capacity,
                ),

                technology_block(
                    name="Gas",
                    icon="gas.png",
                    price_slider_id="gas_price",
                    quantity_slider_id="gas_quantity",
                    price=initial_gas_price,
                    quantity=initial_gas_capacity,
                ),

                technology_block(
                    name="Nuclear",
                    icon="nuclear.png",
                    price_slider_id="nuclear_price",
                    quantity_slider_id="nuclear_quantity",
                    price=initial_nuclear_price,
                    quantity=initial_nuclear_capacity,
                ),
            ],
            style={
                "display": "flex",
                "justify-content": "center",
                "flex-wrap": "wrap",  # 👈 importante para pantallas pequeñas
            }
        ),






        # ---------- Gráfica y resultados ----------
        dcc.Graph(id="market_curve"),
        html.Div(
            id="market_info",
            style={"margin-top": "20px", "font-weight": "bold"}
        ),
    ],
    style={"width": "60%", "margin": "auto"},
)

# =====================
# Callback
# =====================
@app.callback(
    Output("market_curve", "figure"),
    Output("market_info", "children"),
    Input("gas_price", "value"),
    Input("gas_quantity", "value"),
    Input("nuclear_price", "value"),
    Input("nuclear_quantity", "value"),
)
def update_market_curve(
    gas_price,
    gas_quantity,
    nuclear_price,
    nuclear_quantity,
):
    # Construir ofertas
    offers = {
        "gas": {
            "price": gas_price,
            "capacity": gas_quantity,
        },
        "nuclear": {
            "price": nuclear_price,
            "capacity": nuclear_quantity,
        },
    }

    # Curvas de oferta y demanda
    offer_x, offer_y = step_offer_curve_data(offers)
    demand_x, demand_y = step_demand_curve_data(demand_dict)

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

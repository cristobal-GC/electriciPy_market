from dash import Dash, html, dcc, Input, Output
from src.config.parameters import load_scenario
from src.plotting.data import step_offer_curve_data, step_demand_curve_data
from src.plotting.plot import plot_market_curve
import numpy as np

# Cargar escenario
scenario = load_scenario()

# Parámetros iniciales
initial_gas_price = scenario["technologies"]["gas"]["price"]
initial_gas_capacity = scenario["technologies"]["gas"]["capacity"]
initial_nuclear_price = scenario["technologies"]["nuclear"]["price"]
nuclear_capacity = scenario["technologies"]["nuclear"]["capacity"]

demand_dict = scenario["demand"]

# Crear app
app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1("Mercado eléctrico: oferta y demanda escalonada"),

        html.Div([
            html.Label("Precio del gas (€/MWh)"),
            dcc.Slider(
                id="gas_price_slider",
                min=0,
                max=200,
                step=5,
                value=initial_gas_price,
                marks={0: "0", 50: "50", 100: "100", 150: "150", 200: "200"}
            ),
        ], style={"margin-bottom": "20px"}),

        html.Div([
            html.Label("Cantidad ofertada por el gas (MWh)"),
            dcc.Slider(
                id="gas_capacity_slider",
                min=0,
                max=300,
                step=10,
                value=initial_gas_capacity,
                marks={0: "0", 100: "100", 200: "200", 300: "300"}
            ),
        ], style={"margin-bottom": "20px"}),

        html.Div([
            html.Label("Precio de la nuclear (€/MWh)"),
            dcc.Slider(
                id="nuclear_price_slider",
                min=0,
                max=200,
                step=5,
                value=initial_nuclear_price,
                marks={0: "0", 50: "50", 100: "100", 150: "150", 200: "200"}
            ),
        ], style={"margin-bottom": "40px"}),

        dcc.Graph(id="market_curve"),
        html.Div(id="market_info", style={"margin-top": "20px", "font-weight": "bold"})
    ],
    style={"width": "60%", "margin": "auto"}
)

@app.callback(
    Output("market_curve", "figure"),
    Output("market_info", "children"),
    Input("gas_price_slider", "value"),
    Input("gas_capacity_slider", "value"),
    Input("nuclear_price_slider", "value")
)
def update_market_curve(gas_price, gas_capacity, nuclear_price):
    # Construir ofertas
    offers = {
        "gas": {"price": gas_price, "capacity": gas_capacity},
        "nuclear": {"price": nuclear_price, "capacity": nuclear_capacity}
    }

    # Generar datos de curvas
    offer_x, offer_y = step_offer_curve_data(offers)
    demand_x, demand_y = step_demand_curve_data(demand_dict)

    # Calcular precio de casación aproximado
    clearing_price = None
    for px, py in zip(offer_x, offer_y):
        demand_at_px = np.interp(px, demand_x, demand_y)
        if py >= demand_at_px:
            clearing_price = py
            break
    if clearing_price is None:
        clearing_price = offer_y[-1]

    # Generar figura
    fig = plot_market_curve(offer_x, offer_y, demand_x, demand_y, clearing_price)

    info_text = f"Precio de casación aproximado: {clearing_price} €/MWh"

    return fig, info_text

if __name__ == "__main__":
    app.run(debug=True)

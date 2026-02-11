

from dash import html, dcc


def public_info_block(expected_demand, hydro_reserves, co2_price):

    label_style = {
        "fontSize": "20px",
        "marginBottom": "6px",
        "display": "block"
    }

    input_style = {
        "fontSize": "20px",
        "padding": "6px 10px",
        "width": "180px"
    }

    return html.Div(
        [
            html.H2(
                "Public information",
                style={"marginBottom": "25px"}
            ),

            # =====================
            # Expected demand
            # =====================
            html.Div(
                [
                    html.Label(
                        "Expected demand:",
                        style=label_style
                    ),
                    html.Div(
                        f"{expected_demand} GWh",
                        style={
                            "fontSize": "24px",
                            "fontWeight": "bold"
                        }
                    )
                ],
                style={"marginBottom": "25px"}
            ),
            
            # =====================
            # CO2 price
            # =====================
            html.Div(
                [
                    html.Label(
                        "CO₂ price:",
                        style=label_style
                    ),
                    html.Div(
                        f"{co2_price} €/t",
                        style={
                            "fontSize": "24px",
                            "fontWeight": "bold",
                            "marginTop": "5px"
                        }
                    )
                ],
                style={"marginBottom": "25px"}
            ),

            # =====================
            # Hydro reserves
            # =====================
            html.Div(
                [
                    html.Label(
                        "Hydro reserves (GWh):",
                        style=label_style
                    ),
                    dcc.Input(
                        id={"type": "hydro-reserve"},
                        type="number",
                        value=hydro_reserves,
                        min=0,
                        debounce=True,
                        style=input_style
                    ),
                ],
                style={"marginBottom": "25px"}
            ),
          
        ],
        style={
            "border": "1px solid #ccc",
            "borderRadius": "10px",
            "padding": "25px",
            "width": "450px",
            "backgroundColor": "#ECF1F7"
        }
    )


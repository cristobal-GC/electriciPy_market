
from dash import html, dcc


def market_block(expected_demand, hydro_reserves):

    return html.Div(
        [
            html.H3("Market conditions"),

            html.Div(
                [
                    html.Label("Expected demand (MWh)"),
                    html.Div(
                        f"{expected_demand}",
                        style={
                            "fontSize": "20px",
                            "fontWeight": "bold",
                            "marginTop": "5px"
                        }
                    )
                ],
                style={"marginBottom": "15px"}
            ),

            html.Div(
                [
                    html.Label("Hydro reserves (MWh)"),
                    dcc.Input(
                        id={"type": "hydro-reserve"},
                        type="number",
                        value=hydro_reserves,
                        min=0,
                        # step=1,
                        debounce=True
                    )
                ]
            )
        ],
        style={
            "border": "1px solid #ccc",
            "borderRadius": "10px",
            "padding": "15px",
            "width": "250px",
            "backgroundColor": "#F7F9FC"
        }
    )

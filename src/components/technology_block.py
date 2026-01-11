from dash import html
from src.components.sliders import technology_slider

def technology_block(
    *,
    name: str,
    technology: str,
    scenario: dict,
    icon: str,
    quantity_slider_id: str,
    price_slider_id: str,    
):
    """
    Generic block for a generic technology
    """


    ### Retrieve scenario parameters
    quantity_min        = scenario["technologies"][technology]["capacity_min"]
    quantity_max        = scenario["technologies"][technology]["capacity_max"]
    quantity_initial    = scenario["technologies"][technology]["quantity_initial"]
    quantity_step       = scenario["quantity_step"]    
    price_max           = scenario["price_max"]
    price_initial       = scenario["technologies"][technology]["price_initial"]
    price_step          = scenario["price_step"]


    ### Non-scenario parameters
    price_min = 0


    return html.Div(
        [
            html.Img(
                src=f"/assets/icons/{icon}",
                style={"width": "80px"}                
            ),

            html.H2(name),

            technology_slider(
                label="Energy(GWh)",
                slider_id=quantity_slider_id,
                min_value=quantity_min,
                max_value=quantity_max,
                step=quantity_step,
                value=quantity_initial,
                marks={
                    quantity_min: str(quantity_min),
                    quantity_max: str(quantity_max),
                },
                icon=None
            ),

            technology_slider(
                label="Price (EUR/MWh)",
                slider_id=price_slider_id,
                min_value=price_min,
                max_value=price_max,
                step=price_step,
                value=price_initial,
                marks={
                    0: str(0),
                    price_max: str(price_max),
                },
                icon=None
            ),            

        ],
        style={
            "border": "1px solid #ddd",
            "padding": "15px",
            "margin-bottom": "25px",
            "border-radius": "6px",
            "width": "350px",
        }
    )

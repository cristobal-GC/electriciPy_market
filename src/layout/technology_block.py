
from dash import html
from src.layout.technology_slider import technology_slider



def technology_block(
    *,
    tech_key: str,
    tech_dic: dict,
    config_dic: dict
):
    """
    Generic block for a generic technology
    """


    ### Retrieve relevant parameters
    name                = tech_dic["name"]
    quantity_min        = tech_dic["capacity_min"]
    quantity_max        = tech_dic["capacity_max"]
    quantity_initial    = tech_dic["quantity_initial"]
    price_initial       = tech_dic["price_initial"]
    icon                = tech_dic["icon"]
    quantity_step       = config_dic["quantity_step"]    
    price_max           = config_dic["price_max"]
    price_step          = config_dic["price_step"]


    ### Non-scenario parameters
    price_min = 0


    return html.Div(
        [
            html.Img(
                src=f"/assets/icons/{icon}",
                style={"width": "120px"}                
            ),

            html.H2(name),

            technology_slider(
                label="Energy (GWh)",                
                slider_id={
                    "type": "tech-slider",
                    "tech": tech_key,
                    "field": "quantity",
                },
                min_value=quantity_min,
                max_value=quantity_max,
                step=quantity_step,
                value=quantity_initial,
                marks={
                    quantity_min: {"label": str(quantity_min), "style": {"fontSize": "20px"}},  # Fix Marker size 
                    quantity_max: {"label": str(quantity_max), "style": {"fontSize": "20px"}},  # Fix Marker size 
                },
                icon=None
            ),

            technology_slider(
                label="Price (EUR/MWh)",
                slider_id={
                    "type": "tech-slider",
                    "tech": tech_key,
                    "field": "price",
                },                                
                min_value=price_min,
                max_value=price_max,
                step=price_step,
                value=price_initial,
                marks={
                    0: {"label": str(0), "style": {"fontSize": "20px"}},                  # Fix Marker size 
                    price_max: {"label": str(price_max), "style": {"fontSize": "20px"}}   # Fix Marker size 
                },
                icon=None
            ),            

        ],
        style={
            "border": "1px solid #ddd",
            "padding": "15px",
            "margin-bottom": "5px",   # Vertical separation between rows of blocks
            "border-radius": "10px",
            "width": "450px",
        }
    )

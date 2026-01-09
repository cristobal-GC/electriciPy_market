from dash import html
from src.components.sliders import technology_slider

def technology_block(
    *,
    name: str,
    icon: str,
    price_slider_id: str,
    quantity_slider_id: str,
    price: float,
    quantity: float,
    price_range=(0, 200, 5),
    quantity_range=(0, 300, 10),
):
    """
    Bloque completo de una tecnología:
    - Icono
    - Slider de precio
    - Slider de cantidad
    """

    return html.Div(
        [
            html.H3(name),

            technology_slider(
                label="Precio (€/MWh)",
                slider_id=price_slider_id,
                min_value=price_range[0],
                max_value=price_range[1],
                step=price_range[2],
                value=price,
                marks={
                    price_range[0]: str(price_range[0]),
                    price_range[1]: str(price_range[1]),
                },
                icon=icon
            ),

            technology_slider(
                label="Energía ofertada (MWh)",
                slider_id=quantity_slider_id,
                min_value=quantity_range[0],
                max_value=quantity_range[1],
                step=quantity_range[2],
                value=quantity,
                marks={
                    quantity_range[0]: str(quantity_range[0]),
                    quantity_range[1]: str(quantity_range[1]),
                },
                icon=None  # el icono solo una vez
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

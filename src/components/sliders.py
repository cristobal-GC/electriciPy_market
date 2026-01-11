from dash import html, dcc

def technology_slider(
    *,
    label: str,
    slider_id: str,
    min_value: float,
    max_value: float,
    step: float,
    value: float,
    marks: dict,
    icon: str | None = None,
    width: str = "300px"
):
    """
    Generic slider for a generic technology
    """

    if min_value==max_value:
        width='0px'


    slider_block = html.Div(
        [
            html.Label(label),
            dcc.Slider(
                id=slider_id,
                min=min_value,
                max=max_value,
                step=step,
                value=value,
                marks=marks,
                tooltip={"placement": "bottom",
                         "always_visible": True,
                         "style": {"color": "White", "fontSize": "18"}
                         }
            ),
        ],
        style={"width": width}
    )

    if icon is None:
        return slider_block

    return html.Div(
        [
            slider_block,
            html.Img(
                src=f"{icon}",
                style={
                    "height": "60px",
                    "margin-left": "20px"
                }
            ),
        ],
        style={
            "display": "flex",
            "align-items": "center",
            "margin-bottom": "30px"
        }
    )

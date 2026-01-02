import plotly.graph_objects as go

def plot_market_curve(offer_x, offer_y, demand_x, demand_y, clearing_price=None):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=offer_x, y=offer_y,
        mode="lines+markers",
        line_shape="vh",
        name="Oferta"
    ))

    fig.add_trace(go.Scatter(
        x=demand_x, y=demand_y,
        mode="lines+markers",
        line_shape="vh",
        name="Demanda",
        line=dict(color="green")
    ))

    if clearing_price is not None:
        fig.add_hline(
            y=clearing_price,
            line_dash="dash",
            line_color="red",
            annotation_text="Precio casación",
            annotation_position="top right"
        )

    fig.update_layout(
        xaxis_title="Cantidad (MWh)",
        yaxis_title="Precio (€/MWh)",
        title="Mercado eléctrico: Oferta y Demanda"
    )

    return fig

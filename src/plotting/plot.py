import plotly.graph_objects as go

def plot_market_curve(supply_x, supply_y, demand_x, demand_y, clearing_price=None):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=supply_x, y=supply_y,
        mode="lines+markers",
        line_shape="vh",
        name="Supply"
    ))

    fig.add_trace(go.Scatter(
        x=demand_x, y=demand_y,
        mode="lines+markers",
        line_shape="vh",
        name="Demand",
        line=dict(color="green")
    ))

    if clearing_price is not None:
        fig.add_hline(
            y=clearing_price,
            line_dash="dash",
            line_color="red",
            annotation_text="Market clearing price",
            annotation_position="top right"
        )

    fig.update_layout(
        xaxis_title="Energy (MWh)",
        yaxis_title="Price (€/MWh)",
        title="Supply and demand curves",
        width=1200,
        height=800,
    )

    return fig

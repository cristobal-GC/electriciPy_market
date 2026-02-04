import pandas as pd
import plotly.graph_objects as go

def plot_market_curves(df_supply: pd.DataFrame, df_demand: pd.DataFrame) -> go.Figure:
    """
    Dibuja la curva de oferta y la curva de demanda en la misma figura.
    Ambos DataFrames deben tener columnas:
        - 'price'
        - 'quantity'
    """
    # --- Curva de oferta ---
    df_supply_sorted = df_supply.sort_values("price").copy()
    df_supply_sorted["cum_quantity_start"] = df_supply_sorted["quantity"].cumsum() - df_supply_sorted["quantity"]
    df_supply_sorted["cum_quantity_end"] = df_supply_sorted["quantity"].cumsum()

    x_supply = []
    y_supply = []
    for _, row in df_supply_sorted.iterrows():
        x_supply.extend([row["cum_quantity_start"], row["cum_quantity_end"]])
        y_supply.extend([row["price"], row["price"]])

    # --- Curva de demanda ---
    df_demand_sorted = df_demand.sort_values("price", ascending=False).copy()
    df_demand_sorted["cum_quantity_start"] = df_demand_sorted["quantity"].cumsum() - df_demand_sorted["quantity"]
    df_demand_sorted["cum_quantity_end"] = df_demand_sorted["quantity"].cumsum()

    x_demand = []
    y_demand = []
    for _, row in df_demand_sorted.iterrows():
        x_demand.extend([row["cum_quantity_start"], row["cum_quantity_end"]])
        y_demand.extend([row["price"], row["price"]])

    # --- Crear figura ---
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x_supply,
            y=y_supply,
            mode="lines",
            name="Oferta",
            line_shape="hv",
            marker=dict(color="green")
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x_demand,
            y=y_demand,
            mode="lines",
            name="Demanda",
            line_shape="hv",
            marker=dict(color="red")
        )
    )

    # Ajustes de layout
    max_price = max(df_supply_sorted["price"].max(), df_demand_sorted["price"].max()) * 1.05
    fig.update_layout(
        title="Curva de Mercado",
        xaxis_title="Cantidad acumulada (MWh)",
        yaxis_title="Precio (EUR)",
        yaxis=dict(range=[0, max_price]),
        template="plotly_white",
        height=500
    )

    return fig




# import pandas as pd
# import plotly.graph_objects as go


# def plot_market_curve(df_supply: pd.DataFrame) -> go.Figure:
#     """
#     Construye una figura de Plotly con la curva de oferta escalonada correctamente.
#     Cada escalón empieza donde terminó el anterior y tiene altura = precio de la oferta.

#     Parámetros
#     ----------
#     df_supply : pd.DataFrame
#         DataFrame con columnas:
#             - 'technology' (opcional)
#             - 'price' : precio de la oferta
#             - 'quantity' : cantidad ofrecida

#     Retorna
#     -------
#     go.Figure
#         Figura de Plotly con la curva de oferta escalonada.
#     """

#     # Ordenar por precio ascendente
#     df_sorted = df_supply.sort_values("price").copy()

#     # Calcular cantidad acumulada
#     df_sorted["cum_quantity_start"] = df_sorted["quantity"].cumsum() - df_sorted["quantity"]
#     df_sorted["cum_quantity_end"] = df_sorted["quantity"].cumsum()

#     # Construir los puntos de la curva escalonada
#     x_points = []
#     y_points = []

#     for _, row in df_sorted.iterrows():
#         # Escalón horizontal desde el inicio hasta el final de esta oferta
#         x_points.extend([row["cum_quantity_start"], row["cum_quantity_end"]])
#         y_points.extend([row["price"], row["price"]])

#     # Crear figura
#     fig = go.Figure()
#     fig.add_trace(
#         go.Scatter(
#             x=x_points,
#             y=y_points,
#             mode="lines",
#             name="Oferta",
#             line_shape="hv",  # escalón horizontal-vertical
#             marker=dict(color="green")
#         )
#     )

#     # Fijar eje vertical desde 0 hasta un poco más que el máximo precio
#     max_price = df_sorted["price"].max() * 1.05  # +5% margen
#     fig.update_layout(
#         title="Curva de Oferta",
#         xaxis_title="Cantidad acumulada (MWh)",
#         yaxis_title="Precio (EUR)",
#         yaxis=dict(range=[0, max_price]),
#         template="plotly_white",
#         height=700  # fijo en 500px
#     )

#     return fig

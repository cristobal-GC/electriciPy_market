import pandas as pd
import plotly.graph_objects as go

def plot_market_curves(df_supply: pd.DataFrame,
                       df_demand: pd.DataFrame,
                       clearing_price: float,
                       cleared_quantity: float) -> go.Figure:
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
            mode="lines+markers",
            name="Supply",
            line_shape="hv",
            line=dict(color="green", width=3),  # <--- grosor de línea
            marker=dict(color="green", symbol="circle", size=10)
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x_demand,
            y=y_demand,
            mode="lines+markers",
            name="Demand",
            line_shape="hv",
            line=dict(color="red", width=3),  # <--- grosor de línea
            marker=dict(color="red", symbol="circle", size=10)
        )
    )

    # --- Punto de clearing ---
    fig.add_trace(
        go.Scatter(
            x=[cleared_quantity],
            y=[clearing_price],
            mode="markers",
            name="Market clearing",
            marker=dict(color="black",
                        size=15,           
                        symbol="diamond-open",
                        line=dict(width=3)
            )
        )
    )

    # --- Línea vertical (cantidad clearing) ---
    fig.add_trace(
        go.Scatter(
            x=[cleared_quantity, cleared_quantity],
            y=[0, clearing_price],
            mode="lines",
            showlegend=False,
            line=dict(
                color="black",
                dash="dot",
                width=1
            )
        )
    )

    # --- Línea horizontal (precio clearing) ---
    fig.add_trace(
        go.Scatter(
            x=[0, cleared_quantity],
            y=[clearing_price, clearing_price],
            mode="lines",
            showlegend=False,
            line=dict(
                color="black",
                dash="dot",
                width=1
            )
        )
    )

    # Ajustes de layout
    max_price = max(df_supply_sorted["price"].max(), df_demand_sorted["price"].max()) * 1.05
    fig.update_layout(
        #title="Curva de Mercado",
        xaxis_title="Energy (MWh)",
        yaxis_title="Price (€/MWh)",
        xaxis=dict(tickfont=dict(size=22),   # tamaño de números eje x
                   title_font=dict(size=26)  # tamaño del título del eje x
        ),
        yaxis=dict(range=[-2, max_price],
                   tickfont=dict(size=22),   # tamaño de números eje y
                   title_font=dict(size=26)  # tamaño del título del eje y
        ),
        legend=dict(x=0.70,        # posición horizontal (0=izquierda, 1=derecha)
                    y=0.97,        # posición vertical (0=abajo, 1=arriba)
                    bgcolor="rgba(255,255,255,0.7)",  # fondo semitransparente
                    bordercolor="black",
                    borderwidth=1,
                    font=dict(size=18)
        ),        
        template="plotly", # "plotly_white",
        height=700,
        #width=1200
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

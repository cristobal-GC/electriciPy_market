
import pandas as pd
import os
import re

from datetime import datetime

from dash import Dash, html, dcc, dash_table, Input, Output, State, ALL, ctx

from src.config.parameters import load_scenario
from src.layout.dispatch_table_format import dispatch_table_format
from src.layout.public_info_block import public_info_block
from src.layout.technology_block import technology_block
from src.market.build_df_demand import build_df_demand
from src.market.build_df_supply import build_df_supply
from src.market.clear_market import clear_market
from src.market.dispatch_table import dispatch_table
from src.market.estimate_demand import estimate_demand
from src.plotting.plot_market_curves import plot_market_curves





# =====================
# Load scenario
# =====================
scenario = load_scenario("Round_4_LastRound_vGeoConflict_and_ETS")

### Unwrap relevant scenario variables
technologies_dic = scenario["technologies"]
demand_dic = scenario["demand"]
public_info_dic = scenario["public_info"]
config_dic = scenario["config"]

co2_price = public_info_dic["co2_price"]
demand_uncertainty = config_dic["demand_uncertainty"]

### Estimate expected demand
expected_demand = estimate_demand(demand_dic, demand_uncertainty)





# =====================
# Launch app
# =====================
app = Dash(__name__)





# =====================
# App layout
# =====================
app.layout = html.Div(
    [
        # =====================
        # Title
        # =====================
        html.Div(
            html.H1(
                scenario["name"],
                style={
                    "fontSize": "42px",
                    "color": "#1F3A5F",
                    "fontWeight": "700",
                    "marginLeft": "30px"   # Indent
                }
            ),
            style={
                "marginBottom": "30px"
            }
        ),


        # =====================
        # Technology blocks
        # =====================
        html.Div(
            [
                # MarPublic info block
                public_info_block(
                    expected_demand=expected_demand,
                    hydro_reserves=public_info_dic["hydro_reserves"],
                    co2_price=public_info_dic["co2_price"]
                ),

                # Technology blocks
                html.Div(
                    [
                        technology_block(
                            tech_key=tech_key,
                            tech_dic=tech_value,
                            config_dic=config_dic
                        )
                        for tech_key, tech_value in technologies_dic.items()
                    ],
                    style={
                        "display": "flex",
                        "flexWrap": "wrap",
                        "gap": "30px"
                    }
                ),
            ],
            style={
                "display": "flex",
                "justifyContent": "center",
                "alignItems": "flex-start",
                "gap": "30px",
                "marginBottom": "150px"
            }
        ),


        # =====================
        # Graph + Table side-by-side
        # =====================
        html.Div(
            [
                # --- Plot ---
                html.Div(
                    dcc.Graph(id="market_curve"),
                    style={
                        "width": "40%",                     # figure width
                        #"flex": 1,
                        "marginRight": "10px"               # gap between figure and table
                    }
                ),

                # --- Table ---
                html.Div(
                    dash_table.DataTable(
                        id="results_table",
                        page_size=20,
                        style_cell={
                            'fontSize': 20,
                            'fontFamily': 'sans-serif',
                            'textAlign': 'center',
                            'minWidth': '100px',            # cell width
                            #'maxWidth': '150px'
                        },
                        style_header={
                            'backgroundColor': "#C4DAF1",
                            'fontWeight': 'bold',
                            'fontSize': 22,
                            'textAlign': 'center'
                        },
                         style_data_conditional=dispatch_table_format()
                    ),
                    style={
                        "width": "40%",                     # table width
                        #"flex": 2,
                    }
                ),
            ],
            style={
                "display": "flex",
                "justify-content": "center",
                "align-items": "center",
                "marginBottom": "30px"
            }
        ),


        # =====================
        # Button save results
        # =====================
        html.Div(
            html.Button(
                "Save results",
                id="save_results_button",
                n_clicks=0,
                style={
                    "fontSize": "22px",
                    "padding": "22px 40px",
                    "backgroundColor": "#1F3A5F",
                    "color": "white",
                    "border": "none",
                    "borderRadius": "30px",
                    "cursor": "pointer",
                    "boxShadow": "0px 0px 20px rgba(0,0,0,0.4)",
                    "transition": "all 0.2s ease"
                }
            ),
            style={
                "textAlign": "center",
                "marginBottom": "40px"
            }
        ),

        html.Div(id="save_status")

    ],
    style={"fontFamily": "sans-serif"}
)





# =====================
# App callback
# =====================
#
# Each callback defines inputs and outputs.
# Subsequently, a function (with an arbitrary name) is defined.
# The outputs of that function are connected to the outputs declared in the callback.
# The function is executed every time the inputs change.
# It makes sense to have multiple callbacks if the inputs are different, but that's not necessarily the case here.



# ===================== This callback is to update the market (figure and table)
#
##### Inputs:
# The slider values ​​have structured IDs,
# This allows them to be easily retrieved without needing to be strict about the order

@app.callback(
    Output("market_curve", "figure"),
    Output("results_table", "data"),
    Output("results_table", "columns"),
    Input({"type": "tech-slider", "tech": ALL, "field": ALL}, "value"),  
    Input({"type": "hydro-reserve"}, "value"),  
)


def update_market(slider_values, hydro_reserve_value):   # these variables are not used, but are required in Dash for coherence

    slider_inputs = ctx.inputs_list[0]

    hydro_reserves = ctx.inputs_list[1]["value"]

   
    #################### Put all the slider values into df_supply:
    #
    # id || technology | price | quantity
    # ---++------------+-------+----------
    #  0 || solar      | 30    | 100
    #  1 || wind       | 25    |  80
    #  2 || gas        | 90    | 200
    #    
    df_supply = build_df_supply(slider_inputs)


    #################### Put the demand info from scenario dic into df_demand:
    #
    # id || price | quantity
    # ---++-------+----------
    #  0 || 30    | 100
    #  1 || 25    |  10
    #  2 ||  0    |   5
    #
    df_demand = build_df_demand(demand_dic)


    #################### Clear market
    #
    #    df_supply_cleared : pd.DataFrame
        
    #  technology || price | quantity | remaining | cleared_quantity | clearing_price | market_incomes
    #  -----------++-------+------------+---------+------------------+----------------+----------------
    #   solar     || 30    | 100      |    ...
    #   wind      || 25    |  80      |    ...
    #   gas       || 90    | 200      |    ...    
    #
    clearing_price, cleared_quantity, df_supply_cleared = clear_market(df_supply=df_supply,
                                                                       df_demand=df_demand,
                                                                       )

  
    #################### Make plot
    fig = plot_market_curves(df_supply=df_supply,
                             df_demand=df_demand,
                             clearing_price=clearing_price,
                             cleared_quantity=cleared_quantity)


    #################### Prepare data for monitoring DataTable
    data, columns = dispatch_table(df_supply_cleared=df_supply_cleared.round(2),
                                   technologies_dic=technologies_dic,
                                   config_dic=config_dic,
                                   hydro_reserves=hydro_reserves,
                                   co2_price=co2_price)


    return fig, data, columns



# ===================== This callback is to store incomes from the round results
@app.callback(
    Output("save_status", "children"),
    Input("save_results_button", "n_clicks"),
    State("results_table", "data"),
    prevent_initial_call=True
)


def save_round(n_clicks, table_data):

    if not table_data:
        return 0

    df = pd.DataFrame(table_data).set_index('Variable')

    df_incomes = df.loc[["TOTAL INCOMES"]]

    # File name with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    safe_name = re.sub(r'[^\w\-]', '_', scenario['name'])   # Replace special characters with "_"
    filename = f"{timestamp}_{safe_name}.csv"

    results_folder = config_dic["results_folder"]
    os.makedirs(results_folder, exist_ok=True)

    filepath = os.path.join(results_folder, filename)

    df_incomes.to_csv(filepath, index=False)

    return f"Saved: {filename}"





# =====================
# App run
# =====================
if __name__ == "__main__":
    app.run(debug=True, port=8050)   ##### port by default, 8050






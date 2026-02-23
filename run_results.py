from dash import Dash, html, dash_table, Output, Input
import os
import pandas as pd
from glob import glob

# =======================
# RESULTS PATH
# =======================
results_folder = "results"
if not os.path.exists(results_folder):
    raise ValueError(f"No se encontró la carpeta de resultados: {results_folder}")

# =======================
# MAIN FUNCTION
# =======================
def load_results(results_folder="results"):
    """
    Load all CSV result files from the folder, order them by timestamp,
    add a 'Scenario' column including the timestamp, and a 'TOTAL' row at the end.
    """
    if not os.path.exists(results_folder):
        raise ValueError(f"Results folder not found: {results_folder}")

    # Get all CSV files
    csv_files = glob(os.path.join(results_folder, "*.csv"))
    if not csv_files:
        return pd.DataFrame()

    # Helper to extract timestamp from filename: assumes format YYYYMMDD_HHMMSS_scenario.csv
    def get_timestamp(f):
        base = os.path.basename(f)
        parts = base.split('_')
        if len(parts) < 2:
            return "00000000_000000"  # fallback
        return f"{parts[0]}_{parts[1]}"

    # Sort files by timestamp
    csv_files = sorted(csv_files, key=get_timestamp)

    dfs = []
    scenario_names = []

    for f in csv_files:
        df = pd.read_csv(f)
        dfs.append(df)
        # Scenario name: keep timestamp + scenario name, replace underscores in name by spaces
        base = os.path.basename(f).replace(".csv", "")
        parts = base.split('_', 2)
        if len(parts) == 3:
            scenario_name = f"{parts[0]}_{parts[1]}_{parts[2].replace('_', ' ')}"
        else:
            scenario_name = base
        n_rows = df.shape[0]
        scenario_names.extend([scenario_name] * n_rows)

    # Concatenate all results
    all_results = pd.concat(dfs, ignore_index=True, sort=False)

    # Numeric columns
    numeric_cols = all_results.select_dtypes(include='number').columns

    # Add Scenario column
    all_results['Scenario'] = scenario_names

    # Add TOTAL row at the end
    total_row = pd.DataFrame(all_results[numeric_cols].sum()).T
    total_row['Scenario'] = 'TOTAL'
    all_results = pd.concat([all_results, total_row], ignore_index=True, sort=False)

    # Order columns: Scenario first, then numeric columns by total sum
    sums = all_results[numeric_cols].sum().sort_values(ascending=False)
    ordered_numeric_cols = sums.index.tolist()
    final_columns = ['Scenario'] + ordered_numeric_cols
    all_results = all_results[final_columns]

    # Round numeric columns
    return all_results.round(2)



# =======================
# DASH APP
# =======================
app = Dash(__name__)

app.layout = html.Div(
    [

        # Title
        html.H2("Final Results", style={"textAlign": "center", "margin-bottom": "20px"}),

        # Table
        html.Div(
            dash_table.DataTable(
                id="results-table",
                columns=[],
                data=[],
                style_table={'maxWidth': '1600px', 'margin': 'auto', 'overflowX': 'auto'},
                style_cell={
                    'fontFamily': 'sans-serif',
                    'fontSize': 24,
                    'textAlign': 'center',
                    'padding': '5px'},
                style_header={'backgroundColor': "#3D6194",
                              'color': 'white',
                              'fontWeight': 'bold'},
                style_data_conditional=[
                    {'if': {'filter_query': '{Scenario} = "TOTAL"'},
                    'backgroundColor': "#F9EA94", 'fontWeight': 'bold'}
                ]
            ),
            style={"margin": "auto"}
        ),

        # Update button
        html.Div(
            html.Button(
                "Update table",
                id="update-button",
                n_clicks=0,
                style={"fontSize": "16px", "padding": "10px 20px", "cursor": "pointer"}
            ),
            style={"textAlign": "center", "margin-top": "20px"}
        )
    ],
    style={'fontFamily': 'sans-serif'}
)

# =======================
# CALLBACK to update table
# =======================
@app.callback(
    Output("results-table", "data"),
    Output("results-table", "columns"),
    Input("update-button", "n_clicks")
)
def update_table(n_clicks):
    df = load_results()
    if df.empty:
        return [], []
    columns = [{"name": c, "id": c} for c in df.columns]
    data = df.to_dict('records')
    return data, columns

# =======================
# RUN
# =======================
if __name__ == "__main__":
    app.run(debug=True, port=8051)

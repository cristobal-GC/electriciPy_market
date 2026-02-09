


def dispatch_table_format():


    #################### Cell colors according to blocks
    market_rows = ["Offered energy", "Offered price", "Sold energy", "Market price", "Market incomes"]
    dispatch_rows = ["Generated energy", "Unitary variable costs", "Variable costs"]
    penalty_rows = ["Energy imbalance", "Penalty factor", "Penalty price", "Penalty"]
    income_rows = ["TOTAL INCOMES"]


    def make_style(rows, color):
        query = " || ".join([f'{{Variable}} = "{row}"' for row in rows])
        return {'if': {'filter_query': query}, 'backgroundColor': color}

    style_data_conditional = [
        make_style(market_rows, '#E8F4FA'),       # azul claro
        make_style(dispatch_rows, '#FFF2E0'),     # naranja claro
        make_style(penalty_rows, '#FDECEA'),      # rojo claro
        make_style(income_rows, '#E6F4EA')        # verde claro
    ]



    #################### Rows in bold and text color
    highlight_rows = {
        "Market incomes": "#2890DA",    # azul 
        "Variable costs": "#DA9028",    # naranja 
        "Penalty": "#C61D0A",           # rojo 
        "TOTAL INCOMES": "#27611C"      # verde
    }


    highlight_styles = [
        {
            'if': {'filter_query': f'{{Variable}} = "{row}"'},
            'fontWeight': 'bold',
            'color': color  # mismo que el fondo o ligeramente ajustado
        }
        for row, color in highlight_rows.items()
    ]


    style_data_conditional += highlight_styles



    #################### Add thick lines at the beginning of the block
    block_separators = {
        "Offered energy": "2px solid #000000",
        "Generated energy": "2px solid #000000",
        "Energy imbalance": "2px solid #000000",
        "TOTAL INCOMES": "4px solid #000000"
    }

    separator_styles = [
        {
            'if': {'filter_query': f'{{Variable}} = "{row}"'},
            'borderTop': border
        }
        for row, border in block_separators.items()
    ]

    style_data_conditional += separator_styles


    return style_data_conditional
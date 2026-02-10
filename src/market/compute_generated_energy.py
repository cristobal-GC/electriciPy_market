def compute_generated_energy(tech, technologies_dic, df, hydro_reserves):    

    
    # Nuclear: must generate at maximum capacity
    if tech == "nuclear":
        return technologies_dic[tech]["capacity_max"]


    # Dispatchable tecnhologies: generation matches sold energy
    if tech in ['gas', 'coal']:
        return df.at[tech, "Sold energy"]
    

    # Dispatchable tecnhologies with availability constraints: hydro with hydro_reserves
    if tech == 'hydro':
        return min(
            df.at[tech, "Sold energy"],
            hydro_reserves
        )
    

    # Intermittent generation: the minimum between sold energy and potential generation
    if tech == "solar_wind":
        return min(
            technologies_dic[tech]["potential"],
            df.at[tech, "Sold energy"]
        )


    # Default case: sold energy
    return df.at[tech, "Sold energy"]

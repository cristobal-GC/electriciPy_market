def compute_generated_energy(tech, technologies_dic, df):    

    
    # Nuclear: must generate at maximum capacity
    if tech == "nuclear":
        return technologies_dic[tech]["capacity_max"]


    # Dispatchable tecnhologies: generation matches sold energy
    if tech in ['gas', 'hydro', 'coal']:
        return df.at[tech, "Sold energy"]


    # Intermittent generation: the minimum between sold energy and potential generation
    if tech == "solar_wind":
        return min(
            technologies_dic[tech]["potential"],
            df.at[tech, "Sold energy"]
        )


    # Default case: sold energy
    return df.at[tech, "Sold energy"]

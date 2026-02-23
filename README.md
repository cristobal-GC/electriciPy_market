# electriciPy_market: an open tool for electricity market simulation


This repository contains a **simplified electricity market simulator** designed to help students understand how wholesale power markets work and how to design **optimal bidding strategies**.

![electriciPy market panel 1](/img/panel1.png)
![electriciPy market panel 2](/img/panel2.png)


---

## Purpose

This tool introduces students to the key elements of electricity market design, including:

- Merit order and price formation  
- Supply and demand clearing  
- Strategic bidding decisions  
- Dispatch, costs, penalties, and profit calculation  
- The role of wind/solar forecasts  
- Technical constraints for different generation technologies (e.g. hydro reservoirs, nuclear inflexibility, etc.).

Participants can explore how different bidding strategies affect market outcomes in a controlled and transparent environment.

---

## Scope and Limitations

This project is:

- A teaching tool.
- A strategic learning environment.
- A simplified but structured market framework.

It is not:

- A full regulatory model. 
- A forecasting engine.
- A production-ready market simulator.

The simplifications are deliberate: the goal is to make the economic mechanisms visible and understandable.


---

## Highly Configurable

The simulation is designed to be flexible and adaptable to different teaching needs. You can easily modify:

- Generation technologies and costs.
- Demand levels and uncertainty.
- CO2 price assumptions (e.g. EU ETS).
- Fuel price scenarios and external shocks (e.g. gas prices during geopolitical conflicts).

---

## How to Run

### 1. Install the package manager `pixi`

If you do not have `pixi` installed, run:

```bash
curl -fsSL https://pixi.sh/install.sh | bash
```

### 2. Activate the environment

From the root of the repository:

```bash
pixi shell
```


### 3. Configure the scenario

Before launching the simulator, open `run_market.py` and set the desired scenario configuration file (see the available files in `data/scenarios/`, and create your own scenarios from the template). 

To do so, modify the following line in the script:

```
scenario = load_scenario("scenario_template")
```



### 4. Launch the market simulator


```bash
python run_market.py
```

After launching the script, open the local address shown in the terminal (e.g. `http://127.0.0.1:8050/`) in your web browser.



### 4. Save results

By pressing the `Save results` button, you can store the results of each round in the `results/` folder.


### 5. Generate summary table

To create a summary table from the stored rounds:

```bash
python run_results.py
```

![electriciPy market panel 3](/img/panel3.png)

---

## Classroom Activity: 4-Round Market Game

The repository also includes material to run a **4-round in-class market game** (see the `doc/` folder).

Students take the role of generators and submit bids in successive rounds to maximise their profits. Each round is characterised by specific conditions (expected demand, CO2 price, etc.). In every round, the team in charge of wind generation receives a dedicated forecast for that round.

Across the four rounds, students experience:

- Competitive pressure  
- Strategic adaptation  
- Learning dynamics  
- The trade-off between aggressive and conservative bidding  

This structure promotes active engagement and discussion rather than passive observation.



---

## Contributions

Suggestions, improvements, and extensions are welcome.

If you adapt the tool for your own course, feel free to share feedback or improvements.
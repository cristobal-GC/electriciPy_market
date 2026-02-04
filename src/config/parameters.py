import yaml
from pathlib import Path


def load_scenario(scenario_name="base_case"):

    ### Set in a robust way the path for the scenarios folder
    # __file__          : provides the path of this file, parameters.py
    # Path(__file__)    : converths the path in a Path object of library pathlib
    # .resolve          : gets absolute path
    # .parents[2]       : goes up in the path two levels
    scenario_path = Path(__file__).resolve().parents[2] / "data" / "scenarios"
    scenario_file = f"{scenario_name}.yaml"

    with open(scenario_path / scenario_file, "r") as f:
        scenario = yaml.safe_load(f)

    return scenario

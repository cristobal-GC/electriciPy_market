import yaml
from pathlib import Path


def load_scenario(scenario_name="base_case"):
    scenario_path = Path(__file__).resolve().parents[2] / "data" / "scenarios"
    scenario_file = f"{scenario_name}.yaml"

    with open(scenario_path / scenario_file, "r") as f:
        scenario = yaml.safe_load(f)

    return scenario

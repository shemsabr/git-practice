import json
import yaml
import pandas as pd
from pathlib import Path


with open("SHEM\\uke40\\config.yml") as config:
    config = yaml.safe_load(config)
maks_dager = config["max_days_since_calibration"]
output_fil = config["output_file"]

sensors = pd.read_excel("SHEM\\uke40\\sensors.xlsx")
calibrations = pd.read_csv("SHEM\\uke40\\calibrations.csv")
match = pd.merge(sensors, calibrations, on="sensor_id")

overdue_sensors = match[match["days_since_calibration"] > maks_dager]
records = json.loads(overdue_sensors.to_json(orient="records"))

with open(output_fil, "w") as fil:
    json.dump(records ,indent=2)

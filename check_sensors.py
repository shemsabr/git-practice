import json
import yaml
import pandas as pd
from pathlib import Path


def main():

    # Laste inn konfigurasjon
    # Lagre verdiene i variabler
    with open("SHEM\\uke40\\config.yml") as config:
        config = yaml.safe_load(config)         # safe_load brukes for å unngå kjøring av potensielt skadelig kode
    maks_dager = config["max_days_since_calibration"]
    output_fil = config["output_file"]

    # Laste inn sensor- og kalibreringsdata 
    sensors = pd.read_excel("SHEM\\uke40\\sensors.xlsx")
    calibrations = pd.read_csv("SHEM\\uke40\\calibrations.csv")
    match = pd.merge(sensors, calibrations, on="sensor_id")         # Sammenslår sensor- og kalibreringsdata basert på sensor_id

    # Filtrere ut sensorer som har overskredet maks_dager siden siste kalibrering
    overdue_sensors = match[match["days_since_calibration"] > maks_dager]
    records = json.loads(overdue_sensors.to_json(orient="records"))         # Konverterer DataFrame til en liste av ordbøker (records) som kan lagres i JSON-format

    # Lagre resultatene i en JSON-fil hvor navnet på filen er spesifisert i konfigurasjonen
    with open(output_fil, "w") as fil:
        json.dump(records ,indent=2)

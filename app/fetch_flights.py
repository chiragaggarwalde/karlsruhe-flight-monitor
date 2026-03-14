import requests
import pandas as pd
from pathlib import Path

URL = "https://opensky-network.org/api/states/all"

COLUMNS = [
    "icao24",
    "callsign",
    "origin_country",
    "time_position",
    "last_contact",
    "longitude",
    "latitude",
    "baro_altitude",
    "on_ground",
    "velocity",
    "true_track",
    "vertical_rate",
    "sensors",
    "geo_altitude",
    "squawk",
    "spi",
    "position_source",
]

# Karlsruhe area
LAMIN = 48.0
LAMAX = 49.8
LOMIN = 7.5
LOMAX = 9.8


def fetch_flights():
    params = {
        "lamin": LAMIN,
        "lamax": LAMAX,
        "lomin": LOMIN,
        "lomax": LOMAX,
    }
    response = requests.get(URL, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
    return data.get("states", [])


def make_dataframe(states):
    df = pd.DataFrame(states, columns=COLUMNS)
    df["callsign"] = df["callsign"].fillna("").str.strip()

    df = df[[
        "callsign",
        "origin_country",
        "longitude",
        "latitude",
        "baro_altitude",
        "velocity",
        "on_ground",
    ]]

    df = df.dropna(subset=["longitude", "latitude"])
    df = df.sort_values(by="baro_altitude", ascending=False)

    df["longitude"] = df["longitude"].round(4)
    df["latitude"] = df["latitude"].round(4)
    df["baro_altitude"] = df["baro_altitude"].round(2)
    df["velocity"] = df["velocity"].round(2)

    return df

def save_to_csv(df):
    output_path = Path(__file__).resolve().parent.parent / "data" / "processed" / "flights.csv"
    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    flights = fetch_flights()
    df = make_dataframe(flights)

    save_to_csv(df)

    print("Total Karlsruhe-area flights:", len(df))
    print(df[[
        "callsign",
        "origin_country",
        "longitude",
        "latitude",
        "baro_altitude",
        "velocity",
        "on_ground",
    ]].head(10).to_string(index=False))
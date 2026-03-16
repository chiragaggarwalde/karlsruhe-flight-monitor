import requests
import pandas as pd
from pathlib import Path
from datetime import datetime

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

AREA_PARAMS = {
    "lamin": LAMIN,
    "lamax": LAMAX,
    "lomin": LOMIN,
    "lomax": LOMAX,
}
REQUEST_TIMEOUT = 30
AREA_NAME = "Karlsruhe area"

def fetch_flights():
    print(f"Fetching live flight data for {AREA_NAME}...")
    response = requests.get(URL, params=AREA_PARAMS, timeout=REQUEST_TIMEOUT)
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
    df["fetched_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return df

OUTPUT_FILE = Path(__file__).resolve().parent.parent / "data" / "processed" / "flights.csv"
def save_to_csv(df):
    df.to_csv(OUTPUT_FILE, index=False)

def print_stats(df):
    print("Total flights:", len(df))
    print("Countries:", df["origin_country"].nunique())
    print("Highest altitude:", round(df["baro_altitude"].max(), 2))
    print("Average speed:", round(df["velocity"].mean(), 2))
    print("Lowest altitude:", round(df["baro_altitude"].min(), 2))
    print("Average altitude:", round(df["baro_altitude"].mean(), 2))
    print("On-ground flights:", df["on_ground"].sum())
    print("Flights in air:", (~df["on_ground"]).sum())
    print("Most common country:", df["origin_country"].mode().iloc[0])
    print("Highest speed:", round(df["velocity"].max(), 2))
    print("Lowest speed:", round(df["velocity"].min(), 2))
    print("Unique callsigns:", df["callsign"].nunique())
    print("Missing callsigns:", (df["callsign"] == "").sum())
    print()

def print_top_countries(df):
    print("Top 3 countries by flight count:")
    print(df["origin_country"].value_counts().head(3).to_string())
    print()

def print_top_flight(df):
    top_flight = df.iloc[0]
    print("Highest altitude flight details:")
    print(top_flight.to_string())
    print()

if __name__ == "__main__":
    flights = fetch_flights()
    df = make_dataframe(flights)

    if df.empty:
        print(f"No flights found in {AREA_NAME}.")
    else:
        save_to_csv(df)
        print(f"Saved file: {OUTPUT_FILE.relative_to(Path(__file__).resolve().parent.parent)}")
        print("Rows saved:", len(df))
        print()
        print(f"Total flights in {AREA_NAME}: {len(df)}")
        print()

        print("-" * 40)
        print_stats(df)
        print_top_countries(df)
        print_top_flight(df)

        print("-" * 40)
        print(f"Nearby flights in {AREA_NAME}:")
        print(df[[
            "callsign",
            "origin_country",
            "longitude",
            "latitude",
            "baro_altitude",
            "velocity",
            "on_ground",
            "fetched_at",
        ]].head(5).to_string(index=False))
        print()


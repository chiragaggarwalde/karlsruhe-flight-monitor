import requests
import pandas as pd
from pathlib import Path
from datetime import datetime
import time

# -------------------------
# Config
# -------------------------
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

# Karlsruhe bounding box
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
MAX_RETRIES = 3
AREA_NAME = "Karlsruhe area"

OUTPUT_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "processed"
    / "flights.csv"
)

# -------------------------
# Fetch flights (with retry)
# -------------------------
def fetch_flights():
    print(f"[INFO] Fetching live flight data for {AREA_NAME}...")

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(
                URL,
                params=AREA_PARAMS,
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()

            data = response.json()
            states = data.get("states", [])

            print(f"[SUCCESS] Flights fetched: {len(states)}")
            return states

        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Attempt {attempt} failed: {e}")

            if attempt < MAX_RETRIES:
                print("[INFO] Retrying...")
                time.sleep(2)
            else:
                print("[FAILED] Could not fetch flight data.")
                return []

# -------------------------
# Convert to DataFrame
# -------------------------
def make_dataframe(states):
    if not states:
        return pd.DataFrame()

    df = pd.DataFrame(states, columns=COLUMNS)

    # Clean data
    df["callsign"] = df["callsign"].fillna("").str.strip()
    df["origin_country"] = df["origin_country"].fillna("UNKNOWN")

    df = df[[
        "callsign",
        "origin_country",
        "longitude",
        "latitude",
        "baro_altitude",
        "velocity",
        "on_ground",
    ]]

    # Drop missing coordinates
    df = df.dropna(subset=["longitude", "latitude"])

    # Convert numeric safely
    df["baro_altitude"] = pd.to_numeric(df["baro_altitude"], errors="coerce")
    df["velocity"] = pd.to_numeric(df["velocity"], errors="coerce")

    # Sort
    df = df.sort_values(by="baro_altitude", ascending=False)

    # Round values
    df["longitude"] = df["longitude"].round(4)
    df["latitude"] = df["latitude"].round(4)
    df["baro_altitude"] = df["baro_altitude"].round(2)
    df["velocity"] = df["velocity"].round(2)

    # Timestamp
    df["fetched_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return df

# -------------------------
# Save CSV
# -------------------------
def save_to_csv(df):
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"[INFO] Saved file: {OUTPUT_FILE}")

# -------------------------
# Stats
# -------------------------
def print_stats(df):
    print("\n--- Flight Statistics ---")
    print("Total flights:", len(df))
    print("Countries:", df["origin_country"].nunique())
    print("Highest altitude:", round(df["baro_altitude"].max(), 2))
    print("Lowest altitude:", round(df["baro_altitude"].min(), 2))
    print("Average altitude:", round(df["baro_altitude"].mean(), 2))
    print("Average speed:", round(df["velocity"].mean(), 2))
    print("Highest speed:", round(df["velocity"].max(), 2))
    print("Lowest speed:", round(df["velocity"].min(), 2))
    print("Flights in air:", (~df["on_ground"]).sum())
    print("On-ground flights:", df["on_ground"].sum())
    print("Unique callsigns:", df["callsign"].nunique())
    print("Missing callsigns:", (df["callsign"] == "").sum())

    if not df["origin_country"].mode().empty:
        print("Most common country:", df["origin_country"].mode().iloc[0])

# -------------------------
# Extra Insights
# -------------------------
def print_top_countries(df):
    print("\nTop 3 countries:")
    print(df["origin_country"].value_counts().head(3).to_string())

def print_top_flight(df):
    if df.empty:
        return
    print("\nHighest altitude flight:")
    print(df.iloc[0].to_string())

def print_sample(df):
    print("\nSample flights:")
    print(
        df.head(5)[[
            "callsign",
            "origin_country",
            "longitude",
            "latitude",
            "baro_altitude",
            "velocity",
            "on_ground",
            "fetched_at",
        ]].to_string(index=False)
    )

# -------------------------
# Main (CLI mode)
# -------------------------
def main():
    flights = fetch_flights()
    df = make_dataframe(flights)

    if df.empty:
        print(f"[WARNING] No flights found in {AREA_NAME}.")
        return

    save_to_csv(df)

    print(f"\n[INFO] Total flights in {AREA_NAME}: {len(df)}")

    print("-" * 50)
    print_stats(df)
    print_top_countries(df)
    print_top_flight(df)
    print_sample(df)
    print("-" * 50)


if __name__ == "__main__":
    main()
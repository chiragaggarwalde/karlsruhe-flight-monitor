import streamlit as st
from fetch_flights import fetch_flights, make_dataframe
import pandas as pd
import time

st.set_page_config(page_title="Karlsruhe Flight Monitor", layout="wide")

st.title("✈️ Karlsruhe Flight Monitor")
st.caption("Live flight activity using OpenSky data")

# -------------------------
# Auto-refresh toggle
# -------------------------
auto_refresh = st.checkbox("Enable auto-refresh (every 30s)")

if auto_refresh:
    st.info("Auto-refresh is ON")

# -------------------------
# Fetch Button
# -------------------------
if st.button("Fetch flights") or auto_refresh:

    with st.spinner("Fetching live flights..."):
        flights = fetch_flights()
        df = make_dataframe(flights)

    if df.empty:
        st.warning("No flights found in Karlsruhe area.")
    else:
        st.success("Live data loaded for Karlsruhe area.")

        # -------------------------
        # Data Cleaning
        # -------------------------
        df = df.copy()
        df["callsign"] = df["callsign"].fillna("UNKNOWN").str.strip()
        df["origin_country"] = df["origin_country"].fillna("UNKNOWN")

        df["baro_altitude"] = pd.to_numeric(df["baro_altitude"], errors="coerce")
        df["velocity"] = pd.to_numeric(df["velocity"], errors="coerce")

        # -------------------------
        # Metrics
        # -------------------------
        col1, col2, col3 = st.columns(3)
        col4, col5, col6 = st.columns(3)

        col1.metric("Total flights", len(df))
        col2.metric("Countries", df["origin_country"].nunique())
        col3.metric("Highest altitude", round(df["baro_altitude"].max(), 2))

        col4.metric("Average speed", round(df["velocity"].mean(), 2))
        col5.metric("Flights in air", int((~df["on_ground"]).sum()))
        col6.metric("On-ground flights", int(df["on_ground"].sum()))

        # -------------------------
        # Insights (NEW 🔥)
        # -------------------------
        st.subheader("Flight Insights")

        high_alt = df[df["baro_altitude"] > 10000]
        low_alt = df[df["baro_altitude"] < 1000]

        st.write(f"✈️ High altitude flights (>10,000m): {len(high_alt)}")
        st.write(f"🛬 Low altitude / landing flights (<1,000m): {len(low_alt)}")

        # -------------------------
        # Top Countries
        # -------------------------
        st.subheader("Top 5 countries")

        top_countries = (
            df["origin_country"]
            .value_counts()
            .head(5)
            .reset_index()
        )
        top_countries.columns = ["country", "flight_count"]

        st.dataframe(top_countries, use_container_width=True)

        # -------------------------
        # Map (Improved)
        # -------------------------
        st.subheader("Flight map")

        map_df = df[["latitude", "longitude"]].dropna()

        if not map_df.empty:
            st.map(map_df, zoom=6)
        else:
            st.info("No location data available.")

        # -------------------------
        # Highest Flight
        # -------------------------
        st.subheader("Highest altitude flight")

        top_flight = df.sort_values(
            by="baro_altitude", ascending=False
        ).head(1)

        st.dataframe(top_flight, use_container_width=True)

        # -------------------------
        # Altitude Chart
        # -------------------------
        st.subheader("Top 10 flights by altitude")

        chart_df = (
            df[["callsign", "baro_altitude"]]
            .dropna()
            .sort_values(by="baro_altitude", ascending=False)
            .head(10)
        )

        if not chart_df.empty:
            st.bar_chart(chart_df.set_index("callsign"))

        # -------------------------
        # Filters
        # -------------------------
        st.subheader("Filters")

        col1, col2 = st.columns(2)

        with col1:
            country_options = ["All"] + sorted(
                df["origin_country"].dropna().unique().tolist()
            )
            selected_country = st.selectbox("Select country", country_options)

        with col2:
            callsign_filter = st.text_input("Enter callsign")

        filtered_df = df.copy()

        if selected_country != "All":
            filtered_df = filtered_df[
                filtered_df["origin_country"] == selected_country
            ]

        if callsign_filter:
            filtered_df = filtered_df[
                filtered_df["callsign"]
                .str.contains(callsign_filter.upper(), na=False)
            ]

        # -------------------------
        # Table
        # -------------------------
        st.subheader("Nearby flights table")

        st.dataframe(
            filtered_df.sort_values(by="baro_altitude", ascending=False).head(20),
            use_container_width=True,
        )

        # -------------------------
        # Download
        # -------------------------
        st.download_button(
            "Download CSV",
            filtered_df.to_csv(index=False),
            file_name="karlsruhe_flights.csv",
            mime="text/csv",
        )

    # -------------------------
    # Auto refresh loop
    # -------------------------
    if auto_refresh:
        time.sleep(30)
        st.rerun()
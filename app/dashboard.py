import streamlit as st
from fetch_flights import fetch_flights, make_dataframe

st.title("Karlsruhe Flight Monitor")
st.caption("Live flight activity using OpenSky data")
st.info("Click the button to fetch the latest live flight data.")

if st.button("Fetch flights"):
    with st.spinner("Fetching live flights..."):
        flights = fetch_flights()
        df = make_dataframe(flights)

    if df.empty:
        st.warning("No flights found in Karlsruhe area.")
    else:
        st.success("Live data loaded for Karlsruhe area.")

        col1, col2, col3 = st.columns(3)
        col4, col5, col6 = st.columns(3)

        col1.metric("Total flights", len(df))
        col2.metric("Countries", df["origin_country"].nunique())
        col3.metric("Highest altitude", round(df["baro_altitude"].max(), 2))
        col4.metric("Average speed", round(df["velocity"].mean(), 2))
        col5.metric("Flights in air", int((~df["on_ground"]).sum()))
        col6.metric("On-ground flights", int(df["on_ground"].sum()))

        st.subheader("Top 5 countries")
        st.dataframe(
            df["origin_country"].value_counts().head(5).reset_index(name="flight_count")
        )

        st.subheader("Flight map")
        map_df = df[["latitude", "longitude"]].dropna()
        st.map(map_df)

        st.subheader("Highest altitude flight")
        top_flight = df.sort_values(by="baro_altitude", ascending=False).head(1)
        st.dataframe(top_flight)

        st.subheader("Altitude distribution")
        chart_df = (
            df[["callsign", "baro_altitude"]]
            .sort_values(by="baro_altitude", ascending=False)
            .head(10)
        )
        st.bar_chart(chart_df.set_index("callsign"))

        st.subheader("Filter by country")
        country_options = ["All"] + sorted(df["origin_country"].dropna().unique().tolist())
        selected_country = st.selectbox("Select country", country_options)

        st.subheader("Filter by callsign")
        callsign_filter = st.text_input("Enter callsign")

        filtered_df = df

        if selected_country != "All":
            filtered_df = filtered_df[filtered_df["origin_country"] == selected_country]

        if callsign_filter:
            filtered_df = filtered_df[
                filtered_df["callsign"].str.contains(callsign_filter.upper(), na=False)
            ]

        st.subheader("Nearby flights table")
        st.dataframe(filtered_df.sort_values(by="baro_altitude", ascending=False).head(10))

        st.download_button(
            "Download CSV",
            df.to_csv(index=False),
            file_name="karlsruhe_flights.csv",
            mime="text/csv",
        )
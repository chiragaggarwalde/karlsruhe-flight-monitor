import streamlit as st
from fetch_flights import fetch_flights, make_dataframe

st.title("Karlsruhe Flight Monitor")
st.caption("Live flight activity using OpenSky data")

col1, col2, col3 = st.columns(3)
col4, col5 = st.columns(2)

if st.button("Fetch flights"):
    with st.spinner("Fetching live flights..."):
        flights = fetch_flights()
        df = make_dataframe(flights)

    flights = fetch_flights()
    df = make_dataframe(flights)
    if df.empty:
        st.warning("No flights found in Karlsruhe area.")
    else:
        col1.metric("Total flights", len(df))
        col2.metric("Countries", df["origin_country"].nunique())
        col3.metric("Highest altitude", round(df["baro_altitude"].max(), 2))
        col4.metric("Average speed", round(df["velocity"].mean(), 2))
        col5.metric("Flights in air", int((~df["on_ground"]).sum()))
        st.subheader("Nearby flights table")
        st.dataframe(df.sort_values(by="baro_altitude", ascending=False).head(10))
        st.metric("On-ground flights", int(df["on_ground"].sum()))

        st.subheader("Top 5 countries")
        st.subheader("Flight map")
        map_df = df[["latitude", "longitude"]].dropna()
        st.map(map_df)
        st.dataframe(
            df["origin_country"].value_counts().head(5).reset_index(name="flight_count")
        )
        st.download_button(
            "Download CSV",
            df.to_csv(index=False),
            file_name="karlsruhe_flights.csv",
            mime="text/csv",
        )

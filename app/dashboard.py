import streamlit as st
from fetch_flights import fetch_flights, make_dataframe

st.title("Karlsruhe Flight Monitor")

if st.button("Fetch flights"):
    flights = fetch_flights()
    df = make_dataframe(flights)
    st.metric("Total flights", len(df))
    st.metric("Countries", df["origin_country"].nunique())
    st.metric("Highest altitude", round(df["baro_altitude"].max(), 2))
    st.metric("Average speed", round(df["velocity"].mean(), 2))

    st.subheader("Nearby flights")

    st.dataframe(df.head(10))
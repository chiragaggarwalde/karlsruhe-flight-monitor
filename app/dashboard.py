import streamlit as st
from fetch_flights import fetch_flights, make_dataframe

st.title("Karlsruhe Flight Monitor")

if st.button("Fetch flights"):
    flights = fetch_flights()
    df = make_dataframe(flights)
    st.write(f"Total flights: {len(df)}")
    st.dataframe(df)
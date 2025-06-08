import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
import pydeck as pdk

st.set_page_config(page_title="Wszystkie Wykresy", layout="wide", initial_sidebar_state="expanded")

# Dane przykładowe
df = pd.DataFrame({
    "x": np.arange(1, 101),
    "y1": np.random.randn(100).cumsum(),
    "y2": np.random.randn(100).cumsum()
})

### 1. Wbudowane wykresy Streamlit
st.header("🔹 Wbudowane wykresy")
st.subheader("Line Chart")
st.line_chart(df[["y1", "y2"]])

st.subheader("Bar Chart")
st.bar_chart(df[["y1", "y2"]].abs())

st.subheader("Area Chart")
st.area_chart(df[["y1", "y2"]])


### 3. Plotly
st.header("🔸 Plotly")
fig_plotly = px.line(df, x="x", y=["y1", "y2"], title="Plotly Line Chart")
st.plotly_chart(fig_plotly, use_container_width=True)

### 4. Altair
st.header("🔸 Altair")
df_melted = df.melt(id_vars="x", value_vars=["y1", "y2"], var_name="Seria", value_name="Wartość")
chart = alt.Chart(df_melted).mark_line().encode(
    x="x",
    y="Wartość",
    color="Seria"
).properties(title="Altair Line Chart", width=700)
st.altair_chart(chart)

### 6. PyDeck (Mapa)
st.header("🗺️ PyDeck (mapa punktów)")
map_data = pd.DataFrame({
    'lat': 52.0 + np.random.randn(100) * 0.01,
    'lon': 21.0 + np.random.randn(100) * 0.01
})
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/dark-v9',
    initial_view_state=pdk.ViewState(
        latitude=52.0,
        longitude=21.0,
        zoom=11,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=map_data,
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=100,
        ),
    ],
))

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
import pydeck as pdk

st.set_page_config(page_title="Dashboard z filtrami", layout="wide", initial_sidebar_state="expanded")
st.title("📊 Interaktywny Dashboard Streamlit")

# Sidebar – Filtry
st.sidebar.header("🔧 Filtry")

# Zakres osi X
x_range = st.sidebar.slider("Zakres wartości X", 1, 100, (1, 100))

# Wybór serii danych
selected_cols = st.sidebar.multiselect("Wybierz serie do wykresu:", ["y1", "y2"], default=["y1", "y2"])

# Przełącznik – wygeneruj nowe dane
regenerate = st.sidebar.checkbox("🔄 Wygeneruj nowe dane")

# Dane
@st.cache_data
def generate_data():
    return pd.DataFrame({
        "x": np.arange(1, 101),
        "y1": np.random.randn(100).cumsum(),
        "y2": np.random.randn(100).cumsum()
    })

df = generate_data() if not regenerate else pd.DataFrame({
    "x": np.arange(1, 101),
    "y1": np.random.randn(100).cumsum(),
    "y2": np.random.randn(100).cumsum()
})

# Filtrowanie danych
df_filtered = df[(df["x"] >= x_range[0]) & (df["x"] <= x_range[1])]
df_melted = df_filtered.melt(id_vars="x", value_vars=selected_cols, var_name="Seria", value_name="Wartość")

# --- WYKRESY ---

st.header("📈 Wbudowane wykresy Streamlit")
st.line_chart(df_filtered[selected_cols])
st.bar_chart(df_filtered[selected_cols])
st.area_chart(df_filtered[selected_cols])

st.header("📈 Plotly")
fig_plotly = px.line(df_filtered, x="x", y=selected_cols, title="Plotly Line Chart")
st.plotly_chart(fig_plotly, use_container_width=True)

st.header("📈 Altair")
chart = alt.Chart(df_melted).mark_line().encode(
    x="x",
    y="Wartość",
    color="Seria"
).properties(width=800, height=400, title="Altair Line Chart")
st.altair_chart(chart, use_container_width=True)

st.header("🗺️ PyDeck – Mapa punktów")
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
            get_color='[255, 0, 0, 160]',
            get_radius=100,
        ),
    ],
))

st.success("✅ Wszystkie wykresy zostały załadowane.")

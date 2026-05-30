import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import json, os, sys, random

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from style import STYLE, topbar, gauge_html, PORTOS, CORES, LABELS, buscar_porto

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "sereias.json")
with open(DATA_PATH, encoding="utf-8") as f:
    sereias = json.load(f)

def sereias_proximas(lat_o, lon_o, lat_d, lon_d, margem=4.0):
    resultado = []
    for s in sereias:
        lat_s, lon_s = s["latitude"], s["longitude"]
        lat_min = min(lat_o, lat_d) - margem
        lat_max = max(lat_o, lat_d) + margem
        lon_min = min(lon_o, lon_d) - margem
        lon_max = max(lon_o, lon_d) + margem
        if lat_min <= lat_s <= lat_max and lon_min <= lon_s <= lon_max:
            resultado.append(s)
    return resultado

def run():
    st.markdown(STYLE, unsafe_allow_html=True)
    st.markdown(topbar("mapa"), unsafe_allow_html=True)
    st.markdown('<div class="content">', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Mapa de Atividade Sereia</div>', unsafe_allow_html=True)

    aba1, aba2 = st.tabs(["🗺️ Mapa de atividade", "🧭 Mapa de probabilidade"])

    with aba1:
        col_f, col_i = st.columns([3, 1])
        with col_f:
            if "filtro_risco" not in st.session_state:
                st.session_state.filtro_risco = ["alto", "medio", "baixo"]
            filtro = st.multiselect(
                "Filtrar por risco",
                options=["alto", "medio", "baixo"],
                default=st.session_state.filtro_risco,
                format_func=lambda x: LABELS[x],
                key="filtro_risco",
            )
        filtradas = [s for s in sereias if s["risco"] in filtro]
        with col_i:
            st.metric("Sereias visíveis", len(filtradas))

        mapa = folium.Map(location=[-15.0, -35.0], zoom_start=4, tiles="CartoDB positron")
        folium.TileLayer(
            tiles="https://tiles.openseamap.org/seamark/{z}/{x}/{y}.png",
            name="Rotas náuticas", attr="© OpenSeaMap",
            overlay=True, control=True, opacity=0.7,
        ).add_to(mapa)
        folium.LayerControl(position="topright").add_to(mapa)

        st_folium(mapa, width="100%", height=460, returned_objects=[])

    st.markdown("</div>", unsafe_allow_html=True)

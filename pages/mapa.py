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

    st.markdown("</div>", unsafe_allow_html=True)

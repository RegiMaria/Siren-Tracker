import streamlit as st
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from style import STYLE, topbar

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "sereias.json")
with open(DATA_PATH, encoding="utf-8") as f:
    sereias = json.load(f)

def run():
    st.markdown(STYLE, unsafe_allow_html=True)
    st.markdown(topbar("encyclopedia"), unsafe_allow_html=True)
    st.markdown('<div class="content">', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Enciclopédia de Ameaças</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:var(--text-muted);font-size:14px;margin-top:-14px;margin-bottom:20px">Base de dados de inteligência classificada — 7 espécies catalogadas</p>', unsafe_allow_html=True)

    especie_sel = st.selectbox(
        "Selecione uma espécie para ver a ficha completa",
        options=[""] + [s["especie"] for s in sereias],
        format_func=lambda x: "-- Escolha uma espécie --" if x == "" else f"{next((s['emoji'] for s in sereias if s['especie']==x),'')}{x}",
    )

    st.markdown("</div>", unsafe_allow_html=True)

import streamlit as st
import json, os, sys, random
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from style import STYLE, topbar

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "sereias.json")
with open(DATA_PATH, encoding="utf-8") as f:
    sereias = json.load(f)

def run():
    st.markdown(STYLE, unsafe_allow_html=True)
    st.markdown(topbar("routes"), unsafe_allow_html=True)
    st.markdown('<div class="content">', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Análise Avançada de Rotas</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        origem = st.text_input("Porto de origem", value="Santos, BR")
    with col2:
        destino = st.text_input("Porto de destino", value="Lisboa, PT")
    with col3:
        st.write("")
        analisar = st.button("Gerar Análise 🧭", use_container_width=True)

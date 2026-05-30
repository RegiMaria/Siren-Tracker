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

    if analisar:
        zonas = [
            {"nome": f"Zona de Saída — {origem.split(',')[0]}", "km":"0–800km",    "r":15, "cor":"#2EB8AC", "sp":"Zorah",          "nota":"Trânsito seguro — Zorah avistados, comportamento passivo"},
            {"nome":"Atlântico Central — Convergência",          "km":"800–2400km", "r":52, "cor":"#F39237", "sp":"Rusalka",        "nota":"Temperatura 26°C — favorável a migração Rusalka"},
            {"nome":"Zona de Risco Crítico — Mid-Atlantic",      "km":"2400–3800km","r":87, "cor":"#A43955", "sp":"Merrow + Siren", "nota":"Lua cheia + cluster de 5 Merrow + migração Siren ativa"},
            {"nome":"Aproximação Europa — Mar Aberto",           "km":"3800–5200km","r":41, "cor":"#F39237", "sp":"Selkie",         "nota":"Territórios Selkie intermitentes — atenção a 58°N"},
            {"nome": f"Entrada {destino.split(',')[0]}",         "km":"5200–5800km","r":20, "cor":"#2EB8AC", "sp":"Handwerkskunst", "nota":"Manufactura subaquática — manter 15nm do fundo"},
        ]
        total = int(sum(z["r"] for z in zonas) / len(zonas))
        cor_t = "#A43955" if total>60 else "#F39237" if total>35 else "#2EB8AC"
        badge_t = "risk-high" if total>60 else "risk-med" if total>35 else "risk-low"
        label_t = "ALTO" if total>60 else "MODERADO" if total>35 else "LEVE"

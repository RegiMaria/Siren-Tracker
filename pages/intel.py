import streamlit as st
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from style import STYLE, topbar, sonar_html

def run():
    st.markdown(STYLE, unsafe_allow_html=True)
    st.markdown(topbar("intel"), unsafe_allow_html=True)
    st.markdown('<div class="content">', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Central de Inteligência</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<span class="section-label">Alertas Ativos</span>', unsafe_allow_html=True)
        alertas = [
            ("intel-critical","CRÍTICO — NÍVEL 4","Aumento anormal de agressividade Merrow detectado no Atlântico Norte — cluster de 12 indivíduos em movimento coordenado.","REG-2024-0847 · 14 min atrás · Atlântico Norte 48°N 24°W"),
            ("intel-critical","CRÍTICO — NÍVEL 3","Padrão de migração Siren incomum detectado próximo a águas vulcânicas — comportamento de caça coletiva iniciado.","REG-2024-0851 · 31 min atrás · Açores 38°N 28°W"),
            ("intel-warning","ALERTA — NÍVEL 2","Comportamento territorial Selkie intensificado durante fase lunar atual. Regiões costeiras escocesas em vigilância elevada.","REG-2024-0839 · 1h 12min atrás · Mar do Norte 58°N 3°W"),
            ("intel-warning","ALERTA — NÍVEL 2","Cluster Handwerkskunst detectado próximo a rota comercial transatlântica — artefatos submarinos identificados.","REG-2024-0822 · 2h 45min atrás · Atlântico Central 35°N 40°W"),
            ("intel-info","INFORMATIVO — NÍVEL 1","Grupo Locathah de 34 indivíduos em migração sazonal — comportamento não-hostil confirmado.","REG-2024-0818 · 3h atrás · Caribe 18°N 66°W"),
            ("intel-watch","MONITORAMENTO","Anomalia acústica profunda detectada na fossa de Porto Rico — possível atividade Rusalka não catalogada.","REG-2024-0811 · 4h atrás · Porto Rico 20°N 67°W"),
        ]
        for cls, badge, texto, meta in alertas:
            st.markdown(f'<div class="intel-alert {cls}"><span class="intel-badge">{badge}</span><div class="intel-text">{texto}</div><div class="intel-meta">{meta}</div></div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

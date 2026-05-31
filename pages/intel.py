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
        alertas = [
            ("intel-critical","CRÍTICO — NÍVEL 4","Aumento anormal de agressividade Merrow detectado no Atlântico Norte — cluster de 12 indivíduos em movimento coordenado.","REG-2024-0847 · 14 min atrás · Atlântico Norte 48°N 24°W"),
            ("intel-critical","CRÍTICO — NÍVEL 3","Padrão de migração Siren incomum detectado próximo a águas vulcânicas — comportamento de caça coletiva iniciado.","REG-2024-0851 · 31 min atrás · Açores 38°N 28°W"),
            ("intel-warning","ALERTA — NÍVEL 2","Comportamento territorial Selkie intensificado durante fase lunar atual. Regiões costeiras escocesas em vigilância elevada.","REG-2024-0839 · 1h 12min atrás · Mar do Norte 58°N 3°W"),
            ("intel-warning","ALERTA — NÍVEL 2","Cluster Handwerkskunst detectado próximo a rota comercial transatlântica — artefatos submarinos identificados.","REG-2024-0822 · 2h 45min atrás · Atlântico Central 35°N 40°W"),
            ("intel-info","INFORMATIVO — NÍVEL 1","Grupo Locathah de 34 indivíduos em migração sazonal — comportamento não-hostil confirmado.","REG-2024-0818 · 3h atrás · Caribe 18°N 66°W"),
            ("intel-watch","MONITORAMENTO","Anomalia acústica profunda detectada na fossa de Porto Rico — possível atividade Rusalka não catalogada.","REG-2024-0811 · 4h atrás · Porto Rico 20°N 67°W"),
        ]
        alertas_html = "".join(
            f'<div class="intel-alert {cls}"><span class="intel-badge">{badge}</span>'
            f'<div class="intel-text">{texto}</div>'
            f'<div class="intel-meta">{meta}</div></div>'
            for cls, badge, texto, meta in alertas
        )
        st.markdown(f"""
        <div style="background:#FEFEFE;border:1px solid #DAE3F8;border-radius:12px;padding:16px">
          <span class="section-label">Alertas Ativos</span>
          {alertas_html}
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown('<span class="section-label">Radar Oceânico</span>', unsafe_allow_html=True)
        st.markdown(sonar_html(), unsafe_allow_html=True)
        st.markdown("""
        <div style="background:#FEFEFE;border:1px solid #DAE3F8;border-radius:12px;padding:14px;margin-top:14px">
          <span class="section-label">Zonas de Caça Ativas</span>
          <div style="display:flex;flex-direction:column;gap:7px">
            <div style="display:flex;align-items:center;justify-content:space-between;padding:9px 11px;background:#FEF0F3;border-radius:8px;border-left:3px solid #A43955"><div><div style="font-size:13px;font-weight:600;color:#0B1C33">Atlântico Norte</div><div style="font-size:11px;color:#606060">Merrow · 12 indivíduos · Caça ativa</div></div><span class="risk-badge risk-high" style="font-size:11px;padding:3px 9px">CRÍTICA</span></div>
            <div style="display:flex;align-items:center;justify-content:space-between;padding:9px 11px;background:#FEF0F3;border-radius:8px;border-left:3px solid #A43955"><div><div style="font-size:13px;font-weight:600;color:#0B1C33">Açores — Águas Vulcânicas</div><div style="font-size:11px;color:#606060">Siren · Migração + caça coletiva</div></div><span class="risk-badge risk-high" style="font-size:11px;padding:3px 9px">CRÍTICA</span></div>
            <div style="display:flex;align-items:center;justify-content:space-between;padding:9px 11px;background:#FCF5EB;border-radius:8px;border-left:3px solid #F39237"><div><div style="font-size:13px;font-weight:600;color:#0B1C33">Mar do Norte</div><div style="font-size:11px;color:#606060">Selkie · Territorial · Fase lunar</div></div><span class="risk-badge risk-med" style="font-size:11px;padding:3px 9px">ELEVADA</span></div>
            <div style="display:flex;align-items:center;justify-content:space-between;padding:9px 11px;background:#EFF6FF;border-radius:8px;border-left:3px solid #3B8BD4"><div><div style="font-size:13px;font-weight:600;color:#0B1C33">Caribe</div><div style="font-size:11px;color:#606060">Locathah · Migração · Não hostil</div></div><span class="risk-badge risk-low" style="font-size:11px;padding:3px 9px">MONIT.</span></div>
          </div>
        </div>""", unsafe_allow_html=True)


    st.markdown("""
    <div style="background:#FEFEFE;border:1px solid #DAE3F8;border-radius:12px;padding:16px;margin-top:16px">
      <span class="section-label">Densidade de Naufrágios</span>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px 32px;font-size:12px;margin-top:10px">
        <div>
          <div style="display:flex;justify-content:space-between;margin-bottom:4px"><span style="color:#606060">Atlântico Norte</span><span style="font-weight:600;color:#0B1C33">847</span></div>
          <div class="env-bar"><div class="env-bar-fill" style="width:90%;background:#A43955"></div></div>
        </div>
        <div>
          <div style="display:flex;justify-content:space-between;margin-bottom:4px"><span style="color:#606060">Mediterrâneo</span><span style="font-weight:600;color:#0B1C33">562</span></div>
          <div class="env-bar"><div class="env-bar-fill" style="width:60%;background:#F39237"></div></div>
        </div>
        <div>
          <div style="display:flex;justify-content:space-between;margin-bottom:4px"><span style="color:#606060">Mar do Norte</span><span style="font-weight:600;color:#0B1C33">441</span></div>
          <div class="env-bar"><div class="env-bar-fill" style="width:47%;background:#F39237"></div></div>
        </div>
        <div>
          <div style="display:flex;justify-content:space-between;margin-bottom:4px"><span style="color:#606060">Índico</span><span style="font-weight:600;color:#0B1C33">289</span></div>
          <div class="env-bar"><div class="env-bar-fill" style="width:31%;background:#2EB8AC"></div></div>
        </div>
        <div>
          <div style="display:flex;justify-content:space-between;margin-bottom:4px"><span style="color:#606060">Pacífico</span><span style="font-weight:600;color:#0B1C33">198</span></div>
          <div class="env-bar"><div class="env-bar-fill" style="width:21%;background:#2EB8AC"></div></div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

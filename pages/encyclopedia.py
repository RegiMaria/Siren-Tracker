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
    st.markdown('<p style="color:#606060;font-size:14px;margin-top:-14px;margin-bottom:20px">Base de dados de inteligência classificada — 7 espécies catalogadas</p>', unsafe_allow_html=True)

    if "enc_sel" not in st.session_state:
        st.session_state.enc_sel = None

    # ── ficha detalhada ───────────────────────────────────────────────────────
    if st.session_state.enc_sel:
        s = next((x for x in sereias if x["especie"] == st.session_state.enc_sel), None)
        if s:
            cor = s["color"]
            bg  = s["bg"]
            pct = s["ameaca_pct"]
            rc  = s["risco_class"]

            if st.button("← Voltar para a enciclopédia", key="enc_back"):
                st.session_state.enc_sel = None
                st.rerun()

            st.markdown(f"""
            <div class="card" style="margin-bottom:20px">
              <div style="padding:22px;border-bottom:1px solid #DAE3F8;display:flex;align-items:flex-start;gap:18px;background:{bg}">
                <div style="width:90px;height:90px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:48px;background:{cor}22;border:2px solid {cor}33;flex-shrink:0">{s['emoji']}</div>
                <div style="flex:1">
                  <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px">
                    <h2 style="font-size:22px;font-weight:700;color:#0B1C33">{s['especie']}</h2>
                    <span class="risk-badge {rc}">{s['risco_label']}</span>
                  </div>
                  <div style="font-size:13px;color:#606060;margin-bottom:8px">{s['habitat']}</div>
                  <span class="chip">Profundidade: {s['profundidade']}</span>
                  <span class="chip">Freq.: {s['freq']}</span>
                  <div style="margin-top:8px">
                    <div style="font-size:10px;color:#606060;margin-bottom:3px">NÍVEL DE AMEAÇA</div>
                    <div class="threat-meter"><div class="threat-fill" style="width:{pct}%;background:{cor}"></div></div>
                  </div>
                </div>
              </div>
              <div style="padding:20px;display:grid;grid-template-columns:1fr 1fr;gap:20px">
                <div>
                  <div class="spec-section-title">Biologia e Comportamento</div>
                  <div class="spec-field"><span class="spec-field-key">Alimentação</span><span class="spec-field-val">{s['alimentacao']}</span></div>
                  <div class="spec-field"><span class="spec-field-key">Social</span><span class="spec-field-val">{s['social']}</span></div>
                  <div class="spec-field"><span class="spec-field-key">Migração</span><span class="spec-field-val">{s['migracao']}</span></div>
                  <div class="spec-field"><span class="spec-field-key">Método de caça</span><span class="spec-field-val">{s['caca']}</span></div>
                  <div class="spec-field"><span class="spec-field-key">Agressividade</span><span class="spec-field-val">{s['agressividade']}</span></div>
                  <div class="spec-section-title">Inteligência Tática</div>
                  <div class="spec-field"><span class="spec-field-key">Ataque</span><span class="spec-field-val">{s['ataque']}</span></div>
                  <div class="spec-field"><span class="spec-field-key">Fraquezas</span><span class="spec-field-val">{s['fraquezas']}</span></div>
                  <div class="spec-field"><span class="spec-field-key">Regiões</span><span class="spec-field-val">{s['regioes']}</span></div>
                </div>
                <div>
                  <div class="spec-section-title">Risco por Tipo de Embarcação</div>
                  <div class="spec-field"><span class="spec-field-key">Navios de carga</span><span class="spec-field-val" style="color:{cor}">{s['risco_carga']}</span></div>
                  <div class="spec-field"><span class="spec-field-key">Pescadores</span><span class="spec-field-val" style="color:{cor}">{s['risco_pescadores']}</span></div>
                  <div class="spec-field"><span class="spec-field-key">Militares</span><span class="spec-field-val" style="color:{cor}">{s['risco_militar']}</span></div>
                  <div class="spec-field"><span class="spec-field-key">Incidentes</span><span class="spec-field-val">{s['incidentes']}</span></div>
                  <div class="spec-section-title">Registro de Inteligência</div>
                  <div class="spec-lore">{s['lore']}</div>
                </div>
              </div>
            </div>
            </div>""", unsafe_allow_html=True)
            return

    # ── grid de cards ─────────────────────────────────────────────────────────
    cols = st.columns(3)
    for i, s in enumerate(sereias):
        rc = "tag-high" if s["risco"]=="alto" else "tag-med" if s["risco"]=="medio" else "tag-low"
        with cols[i % 3]:
            st.markdown(f"""
            <div class="spec-card" style="margin-bottom:16px">
              <div class="spec-card-banner" style="background:{s['bg']}">
                <span style="font-size:52px">{s['emoji']}</span>
                <div style="position:absolute;top:10px;right:10px"><span class="spec-tag {rc}">{s['risco_label']}</span></div>
              </div>
              <div class="spec-card-body">
                <div class="spec-card-name">{s['especie']}</div>
                <div style="font-size:12px;color:#606060;margin-bottom:12px">{s['habitat'].split(',')[0]}</div>
              </div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"Ver relatório completo →", key=f"enc_{s['key']}"):
                st.session_state.enc_sel = s["especie"]
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

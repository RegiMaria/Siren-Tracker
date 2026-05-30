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

        col_a, col_b = st.columns([1, 2]) # A lista de todas as espécies com emoji, nome e badge de risco de cada uma isso que importa
        with col_a:
            st.markdown(f"""
            <div style="text-align:center;padding:22px;background:#F8F9FF;border-radius:12px;margin-bottom:14px">
              <div style="font-size:48px;font-weight:700;color:{cor_t}">{total}%</div>
              <div style="font-size:13px;color:var(--text-muted);margin-bottom:6px">Risco médio da rota</div>
              <span class="risk-badge {badge_t}">{label_t}</span>
            </div>
            <span class="section-label">Espécies Encontradas</span>""", unsafe_allow_html=True)

            for s in sereias:
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:7px 9px;background:#F8F9FF;border-radius:8px;font-size:12px;margin-bottom:5px">
                  <span style="font-size:17px">{s['emoji']}</span>
                  <span style="flex:1;font-weight:500">{s['especie']}</span>
                  <span class="risk-badge {s['risco_class']}" style="font-size:10px;padding:2px 7px">{s['risco_label']}</span>
                </div>""", unsafe_allow_html=True)
        
        with col_b:
            st.markdown(f'<span class="section-label">Linha do Tempo — {origem} → {destino}</span>', unsafe_allow_html=True)
            st.markdown('<div class="route-timeline"><div class="rt-header">ANÁLISE SEGMENTO POR SEGMENTO</div>', unsafe_allow_html=True)
            for z in zonas:
                st.markdown(f"""
                <div class="rt-row">
                  <div class="rt-dot" style="background:{z['cor']}"></div>
                  <div>
                    <div style="font-weight:500;color:var(--text-primary);font-size:12px">{z['nome']} <span style="color:var(--text-muted)">({z['km']})</span></div>
                    <div style="color:var(--text-muted);font-size:11px;margin-top:2px">Espécie: <strong>{z['sp']}</strong> · Risco: <strong style="color:{z['cor']}">{z['r']}%</strong></div>
                    <div style="color:var(--text-muted);font-size:11px;margin-top:1px">{z['nota']}</div>
                  </div>
                </div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
# Rota alternativa e segura ou rota moderada. A escolha é sua!
            st.markdown("""
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:10px">
              <div style="padding:11px;background:var(--teal-light);border:1px solid var(--teal-border);border-radius:8px">
                <div style="font-size:11px;font-weight:700;color:#27A468;margin-bottom:3px">🧭 ROTA ALTERNATIVA — SEGURA</div>
                <div style="font-size:12px">Via 28°S desvia da zona crítica. +340km mas reduz risco em 38%.</div>
              </div>
              <div style="padding:11px;background:var(--amber-light);border:1px solid var(--amber-border);border-radius:8px">
                <div style="font-size:11px;font-weight:700;color:#c07a0a;margin-bottom:3px">⚡ ROTA RÁPIDA — MODERADA</div>
                <div style="font-size:12px">Rota direta às 14h-16h UTC reduz exposição Siren em 22%.</div>
              </div>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="padding:50px;text-align:center;color:var(--text-muted);font-size:14px;background:var(--surface);border:1px solid var(--border);border-radius:14px">
          Configure origem e destino e clique em "Gerar Análise" para o relatório completo de risco.
        </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


import streamlit as st
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from style import STYLE, topbar

def run():
    st.markdown(STYLE, unsafe_allow_html=True)
    st.markdown(topbar("reports"), unsafe_allow_html=True)
    st.markdown('<div class="content">', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Relatórios de Inteligência</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
<div style="background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:22px">
<span class="section-label">Relatório Mensal — Maio 2026</span>
<div style="display:flex;flex-direction:column;">
<div style="display:flex;justify-content:space-between;padding:11px 0;border-bottom:1px solid var(--border);font-size:14px"><span style="color:var(--text-muted)">Avistamentos totais</span><span style="font-weight:600">4.847</span></div>
<div style="display:flex;justify-content:space-between;padding:11px 0;border-bottom:1px solid var(--border);font-size:14px"><span style="color:var(--text-muted)">Ataques registrados</span><span style="font-weight:600;color:#A43955">23</span></div>
<div style="display:flex;justify-content:space-between;padding:11px 0;border-bottom:1px solid var(--border);font-size:14px"><span style="color:var(--text-muted)">Embarcações alertadas</span><span style="font-weight:600">1.204</span></div>
<div style="display:flex;justify-content:space-between;padding:11px 0;border-bottom:1px solid var(--border);font-size:14px"><span style="color:var(--text-muted)">Vidas salvas (estimado)</span><span style="font-weight:600;color:#2EB8AC">891</span></div>
<div style="display:flex;justify-content:space-between;padding:11px 0;font-size:14px"><span style="color:var(--text-muted)">Espécie mais ativa</span><span style="font-weight:600;color:#A43955">Merrow</span></div>
</div>
</div>""", unsafe_allow_html=True)

    with col2:
        especies = [
            ("Merrow", 78, "#A43955"),
            ("Siren", 62, "#A43955"),
            ("Selkie", 45, "#F39237"),
            ("Rusalka", 30, "#F39237"),
            ("Handwerkskunst", 20, "#8E9DCC"),
            ("Zorah", 8, "#2EB8AC"),
            ("Locathah", 3, "#2EB8AC"),
        ]
        barras = "".join(
            f'<div style="font-size:13px;display:flex;align-items:center;gap:10px;padding:5px 0">'
            f'<span style="flex:0 0 120px;color:var(--text-muted)">{nome}</span>'
            f'<div class="env-bar" style="flex:1"><div class="env-bar-fill" style="width:{pct}%;background:{cor}"></div></div>'
            f'<span style="font-size:12px;font-weight:600;width:32px;text-align:right">{pct}%</span>'
            f'</div>'
            for nome, pct, cor in especies
        )
        st.markdown(
            '<div style="background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:22px">'
            '<span class="section-label">Incidentes por Espécie</span>'
            '<div style="display:flex;flex-direction:column;gap:4px;margin-top:12px">'
            + barras +
            '</div></div>',
            unsafe_allow_html=True,
        )

    incidentes = [
        ("12 Mai 2026", "risk-high", "Merrow — CRÍTICO",
         "Cargueiro MV Stellarwind atacado a 48°N 24°W — casco danificado, tripulação evacuada com sucesso graças ao alerta Siren Tracker."),
        ("08 Mai 2026", "risk-high", "Siren — ALTO",
         "Embarcação de pesca Esperança desviada a 200nm de zona de canto ativo nas Ilhas Canárias — nenhuma baixa registrada."),
        ("03 Mai 2026", "risk-med", "Selkie — MÉDIO",
         "Traineira OceanHeart relatou avistamento de 8 Selkies em comportamento territorial — rota ajustada preventivamente."),
        ("28 Abr 2026", "risk-low", "Locathah — BAIXO",
         "Migração de 200+ Locathah documentada no Golfo do México — sem incidentes, catalogado para base migratória."),
    ]
    linhas = "".join(
        f'<div style="padding:14px 0;border-bottom:1px solid var(--border);display:grid;grid-template-columns:120px 160px 1fr;gap:16px;align-items:start">'
        f'<span style="font-family:monospace;font-size:12px;color:var(--text-muted);padding-top:3px">{data}</span>'
        f'<span class="risk-badge {rc}" style="width:fit-content;font-size:12px;padding:4px 10px">{label}</span>'
        f'<span style="font-size:14px;line-height:1.5;color:var(--text-primary)">{desc}</span>'
        f'</div>'
        for data, rc, label, desc in incidentes
    )
    st.markdown(
        '<div style="background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:22px;margin-top:14px">'
        '<span class="section-label">Histórico de Incidentes Notáveis</span>'
        + linhas +
        '</div></div>',
        unsafe_allow_html=True,
    )

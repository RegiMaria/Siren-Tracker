import streamlit as st
# Deve ser importado em todas as pages
# ── paleta e CSS ──────────────────────────────────────────────────────────────
STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Rethink+Sans:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap');
:root {
  --bg:#F5F5FA; --surface:#FEFEFE; --border:#DAE3F8;
  --text-primary:#0B1C33; --text-muted:#606060;
  --red:#A43955; --red-light:#FCEBEF; --red-border:#F7C1CE;
  --teal:#2EB8AC; --teal-light:#DCFCE7; --teal-border:#00B69B;
  --amber:#F39237; --amber-light:#FCF5EB; --amber-border:#F7E1C1;
  --navy:#0B3954; --purple:#7B506F; --slate:#8E9DCC;
  --font:'Rethink Sans',sans-serif; --mono:'Space Mono',monospace;
}
html,body,[class*="css"]{font-family:var(--font)!important}
#MainMenu,footer,header,[data-testid="stToolbar"]{visibility:hidden}
.block-container{padding:0 32px!important;max-width:100%!important}
[data-testid="stSidebar"]{display:none!important}

.topbar{background:var(--surface);border-bottom:1px solid var(--border);height:64px;display:flex;align-items:center;justify-content:space-between;padding:0 60px;position:sticky;top:0;z-index:100;margin-left:-32px;margin-right:-32px}
.brand{display:flex;align-items:center;gap:10px;font-size:17px;font-weight:500;color:var(--text-primary)}
.brand-sub{font-size:10px;font-family:var(--mono);color:var(--text-muted);margin-left:4px;opacity:.7}
.nav{display:flex;gap:2px}
.nav a{padding:7px 13px;border-radius:8px;font-size:13px;font-weight:500;color:var(--text-muted);text-decoration:none;transition:.15s;display:flex;align-items:center;gap:5px}
.nav a:hover{background:#F2F5FA;color:var(--navy)}
.nav a.active{background:#EEF2FF;color:#4379EE}
.nav a.locked{color:#ccc;pointer-events:none}
.btn-cad{padding:7px 16px;border:none;border-radius:8px;background:var(--purple);color:#fff;font-size:13px;font-weight:500;cursor:pointer}
.content{padding:28px 32px}
.page-title{font-size:26px;font-weight:600;color:var(--text-primary);margin-bottom:20px}

.stats-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:20px}
.stat-card{background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:18px;display:flex;align-items:center;justify-content:space-between}
.stat-label{font-size:13px;color:var(--text-muted);margin-bottom:6px}
.stat-value{font-size:23px;font-weight:700;color:var(--text-primary)}
.stat-trend{font-size:12px;font-weight:600;margin-top:4px}
.trend-up{color:#00B69B}.trend-down{color:var(--red)}
.stat-icon{width:44px;height:44px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:20px}

.card{background:var(--surface);border:1px solid var(--border);border-radius:14px;overflow:hidden;margin-bottom:14px}
.card-header{padding:18px 18px 0;margin-bottom:10px;display:flex;align-items:center;justify-content:space-between}
.card-title{font-size:16px;font-weight:500;color:var(--text-primary);opacity:.85}

.risk-badge{display:inline-flex;align-items:center;padding:5px 12px;border-radius:8px;font-size:12px;font-weight:500}
.risk-high{background:var(--red-light);border:1px solid var(--red-border);color:#D03258}
.risk-med{background:var(--amber-light);border:1px solid var(--amber-border);color:#d4900a}
.risk-low{background:var(--teal-light);border:1px solid var(--teal-border);color:#27A468}

.note-btn{display:inline-flex;align-items:center;padding:5px 12px;border-radius:8px;font-size:12px;font-weight:500}
.note-danger{background:var(--red);color:#fff}
.note-purple{background:var(--purple);color:#fff}
.note-navy{background:var(--navy);color:#fff}
.note-slate{background:var(--slate);color:var(--navy)}
.note-teal{background:var(--teal);color:#fff}
.note-lavender{background:#E1B7ED;color:var(--purple)}

.species-table{width:100%;border-collapse:collapse;table-layout:fixed}
.species-table th{background:#F2F5FA;padding:12px 18px;text-align:left;font-size:12px;font-weight:600;color:var(--text-muted);border-top:1px solid var(--border);border-bottom:1px solid var(--border)}
.species-table th:nth-child(1){width:22%}
.species-table th:nth-child(2){width:14%}
.species-table th:nth-child(3){width:20%}
.species-table th:nth-child(4){width:44%}
.species-table td{padding:14px 18px;border-bottom:1px solid var(--border);font-size:13px;vertical-align:middle}
.species-table tr:last-child td{border-bottom:none}
.species-table tr:hover td{background:#FAFBFF}

.intel-alert{padding:12px 14px;border-radius:10px;border-left:4px solid;margin-bottom:8px}
.intel-critical{background:#FEF0F3;border-color:var(--red)}
.intel-warning{background:var(--amber-light);border-color:var(--amber)}
.intel-info{background:#EFF6FF;border-color:#3B8BD4}
.intel-watch{background:#F5F0FA;border-color:var(--purple)}
.intel-badge{font-size:10px;font-weight:700;letter-spacing:1.2px;margin-bottom:4px;display:block}
.intel-critical .intel-badge{color:var(--red)}
.intel-warning .intel-badge{color:var(--amber)}
.intel-info .intel-badge{color:#3B8BD4}
.intel-watch .intel-badge{color:var(--purple)}
.intel-text{font-size:13px;line-height:1.5;font-weight:500;color:var(--text-primary)}
.intel-meta{font-size:11px;color:var(--text-muted);margin-top:4px;font-family:var(--mono)}

.enc-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:14px}
.spec-card{background:var(--surface);border:1px solid var(--border);border-radius:12px;overflow:hidden;cursor:pointer;transition:all .2s}
.spec-card:hover{border-color:var(--slate);transform:translateY(-2px);box-shadow:0 6px 20px rgba(11,28,51,.07)}
.spec-card-banner{height:90px;display:flex;align-items:center;justify-content:center;font-size:48px;position:relative}
.spec-card-body{padding:12px}
.spec-card-name{font-size:15px;font-weight:600;color:var(--text-primary);margin-bottom:3px}
.spec-tag{font-size:10px;font-weight:600;padding:2px 7px;border-radius:20px;display:inline-block;margin:2px}
.tag-high{background:var(--red-light);color:var(--red)}
.tag-med{background:var(--amber-light);color:#c07a0a}
.tag-low{background:var(--teal-light);color:#27A468}

.spec-field{display:flex;justify-content:space-between;padding:7px 0;border-bottom:1px solid #F2F5FA;font-size:13px}
.spec-field-key{color:var(--text-muted)}
.spec-field-val{font-weight:500;text-align:right;max-width:55%}
.spec-section-title{font-size:10px;font-weight:700;letter-spacing:1.5px;color:var(--text-muted);text-transform:uppercase;margin:14px 0 8px}
.spec-lore{background:#F8F9FF;border-left:3px solid var(--slate);padding:12px;border-radius:0 8px 8px 0;font-size:12px;line-height:1.7;color:var(--text-muted);font-style:italic}
.threat-meter{height:5px;border-radius:3px;background:#E8EDF5;overflow:hidden;margin-top:3px}
.threat-fill{height:100%;border-radius:3px}
.chip{font-size:11px;padding:3px 9px;border-radius:20px;border:1px solid var(--border);color:var(--text-muted);background:var(--surface);display:inline-block;margin:2px}

.route-timeline{border:1px solid var(--border);border-radius:10px;overflow:hidden;margin-top:10px}
.rt-header{padding:9px 13px;background:#F2F5FA;font-size:11px;font-weight:600;color:var(--text-muted);letter-spacing:.5px}
.rt-row{padding:9px 13px;border-top:1px solid var(--border);display:flex;align-items:flex-start;gap:10px;font-size:12px}
.rt-dot{width:9px;height:9px;border-radius:50%;flex-shrink:0;margin-top:3px}

.ficha-sereia{border-radius:10px;padding:14px 18px;margin-top:10px;border-left:4px solid}
.ficha-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:8px 0}
.ficha-item-label{font-size:10px;color:#888;margin-bottom:2px}
.ficha-item-value{font-size:13px;font-weight:500;color:var(--text-primary)}

.env-bar{height:4px;border-radius:2px;background:#E8EDF5;overflow:hidden}
.env-bar-fill{height:100%;border-radius:2px}
.section-label{font-size:11px;font-weight:700;letter-spacing:1.5px;color:var(--text-muted);text-transform:uppercase;margin-bottom:10px;display:block}
.sonar-widget{background:var(--navy);border-radius:12px;padding:14px}
.sonar-title{color:#8E9DCC;font-size:10px;font-family:var(--mono);letter-spacing:1px;margin-bottom:10px}
.gauge-wrap{position:relative;width:84px;height:84px}
.gauge-wrap svg{width:100%;height:100%}
.gauge-pct{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:19px;font-weight:600;color:var(--text-primary)}
.risk-factor{display:flex;align-items:center;gap:7px;margin:3px 0;font-size:12px;color:var(--text-muted)}
.rfd{width:6px;height:6px;border-radius:50%;flex-shrink:0}
.alt-route{margin-top:8px;padding:9px 11px;background:var(--surface);border:1px solid var(--border);border-radius:8px;font-size:12px}
.alt-label{font-weight:600;color:var(--teal);margin-bottom:2px;font-size:12px}
</style>
"""

LOGO_SVG = """<svg width="30" height="30" viewBox="0 0 40 40">
  <ellipse cx="20" cy="22" rx="14" ry="14" fill="#E1B7ED" opacity=".3"/>
  <path d="M20 8C14 8 9 13 9 19c0 4 2 7 5 9l-2 2h16l-2-2c3-2 5-5 5-9 0-6-5-11-11-11z" fill="#A43955"/>
  <path d="M15 20c0-3 2-5 5-5s5 2 5 5" stroke="#E1B7ED" stroke-width="1.5" fill="none" stroke-linecap="round"/>
  <circle cx="20" cy="19" r="3" fill="#8E9DCC"/>
  <circle cx="20" cy="19" r="1.5" fill="#DAE3F8"/>
  <circle cx="20" cy="19" r=".6" fill="#A43955"/>
</svg>"""

# ── portos pré-calculados ─────────────────────────────────────────────────────
PORTOS = {
    # Brasil
    "santos":         {"lat": -23.9608, "lon": -46.3336, "nome": "Santos, BR"},
    "recife":         {"lat": -8.0476,  "lon": -34.8770, "nome": "Recife, BR"},
    "fortaleza":      {"lat": -3.7172,  "lon": -38.5433, "nome": "Fortaleza, BR"},
    "salvador":       {"lat": -12.9714, "lon": -38.5014, "nome": "Salvador, BR"},
    "rio de janeiro": {"lat": -22.9068, "lon": -43.1729, "nome": "Rio de Janeiro, BR"},
    "belem":          {"lat": -1.4558,  "lon": -48.5044, "nome": "Belém, BR"},
    "natal":          {"lat": -5.7945,  "lon": -35.2110, "nome": "Natal, BR"},
    "florianopolis":  {"lat": -27.5954, "lon": -48.5480, "nome": "Florianópolis, BR"},
    "porto alegre":   {"lat": -30.0346, "lon": -51.2177, "nome": "Porto Alegre, BR"},
    "manaus":         {"lat": -3.1190,  "lon": -60.0217, "nome": "Manaus, BR"},
    # Europa
    "lisboa":         {"lat": 38.7169,  "lon": -9.1399,  "nome": "Lisboa, PT"},
    "porto":          {"lat": 41.1579,  "lon": -8.6291,  "nome": "Porto, PT"},
    "madrid":         {"lat": 40.4168,  "lon": -3.7038,  "nome": "Madrid, ES"},
    "barcelona":      {"lat": 41.3851,  "lon": 2.1734,   "nome": "Barcelona, ES"},
    "paris":          {"lat": 48.8566,  "lon": 2.3522,   "nome": "Paris, FR"},
    "amsterdam":      {"lat": 52.3676,  "lon": 4.9041,   "nome": "Amsterdam, NL"},
    "hamburgo":       {"lat": 53.5753,  "lon": 10.0153,  "nome": "Hamburgo, DE"},
    "londres":        {"lat": 51.5074,  "lon": -0.1278,  "nome": "Londres, UK"},
    "rotterdam":      {"lat": 51.9225,  "lon": 4.4792,   "nome": "Rotterdam, NL"},
    "marselha":       {"lat": 43.2965,  "lon": 5.3698,   "nome": "Marselha, FR"},
    # África
    "luanda":         {"lat": -8.8368,  "lon": 13.2343,  "nome": "Luanda, AO"},
    "cape town":      {"lat": -33.9249, "lon": 18.4241,  "nome": "Cape Town, ZA"},
    "dakar":          {"lat": 14.6928,  "lon": -17.4467, "nome": "Dakar, SN"},
    "lagos":          {"lat": 6.5244,   "lon": 3.3792,   "nome": "Lagos, NG"},
    "mombasa":        {"lat": -4.0435,  "lon": 39.6682,  "nome": "Mombasa, KE"},
    # Américas
    "miami":          {"lat": 25.7617,  "lon": -80.1918, "nome": "Miami, US"},
    "nova york":      {"lat": 40.7128,  "lon": -74.0060, "nome": "Nova York, US"},
    "new york":       {"lat": 40.7128,  "lon": -74.0060, "nome": "Nova York, US"},
    "buenos aires":   {"lat": -34.6037, "lon": -58.3816, "nome": "Buenos Aires, AR"},
    "montevideo":     {"lat": -34.9011, "lon": -56.1915, "nome": "Montevideo, UY"},
    "havana":         {"lat": 23.1136,  "lon": -82.3666, "nome": "Havana, CU"},
    "panama":         {"lat": 8.9824,   "lon": -79.5199, "nome": "Panamá, PA"},
    # Ásia / Oceania
    "dubai":          {"lat": 25.2048,  "lon": 55.2708,  "nome": "Dubai, UAE"},
    "singapura":      {"lat": 1.3521,   "lon": 103.8198, "nome": "Singapura, SG"},
    "toquio":         {"lat": 35.6762,  "lon": 139.6503, "nome": "Tóquio, JP"},
    "sydney":         {"lat": -33.8688, "lon": 151.2093, "nome": "Sydney, AU"},
    "xangai":         {"lat": 31.2304,  "lon": 121.4737, "nome": "Xangai, CN"},
}

CORES  = {"alto": "#A43955", "medio": "#F39237", "baixo": "#2EB8AC"}
LABELS = {"alto": "🔴 Alto risco", "medio": "🟡 Médio risco", "baixo": "🟢 Baixo risco"}

def buscar_porto(texto):
    """Busca porto pelo nome digitado — normaliza acentos e variações."""
    chave = texto.strip().lower()
    # remove sufixos de estado/país
    for sufixo in [", br", ", pt", ", es", ", fr", ", de", ", uk", ", us",
                   ", ao", ", za", ", ng", ", ke", ", sn", ", ar", ", uy",
                   ", cu", ", pa", ", ae", ", sg", ", jp", ", au", ", cn", ", nl"]:
        chave = chave.replace(sufixo, "")
    chave = chave.strip()
    # busca direta
    if chave in PORTOS:
        return PORTOS[chave]
    # busca parcial
    for key, val in PORTOS.items():
        if chave in key or key in chave:
            return val
    return None

def gauge_html(pct, color, label):
    c = 251.2
    offset = c - (c * pct / 100)
    return f"""
    <div style="display:flex;flex-direction:column;align-items:center;gap:5px;">
      <div class="gauge-wrap">
        <svg viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="40" fill="none" stroke="#F2F5FA" stroke-width="12"/>
          <circle cx="50" cy="50" r="40" fill="none" stroke="{color}" stroke-width="12"
            stroke-dasharray="{c}" stroke-dashoffset="{offset}" stroke-linecap="round"
            transform="rotate(-90 50 50)"/>
        </svg>
        <div class="gauge-pct">{pct}%</div>
      </div>
      <div style="font-size:11px;color:var(--text-muted);text-align:center;max-width:100px;line-height:1.3">{label}</div>
    </div>"""

def topbar(pagina_ativa="dashboard"):
    PAGES = [
        ("dashboard",    "🗺️ Dashboard"),
        ("mapa",         "📍 Mapa"),
        ("intel",        "📡 Inteligência"),
        ("encyclopedia", "📖 Enciclopédia"),
        ("routes",       "🧭 Rotas"),
        ("reports",      "📋 Relatórios"),
    ]

    st.markdown(STYLE, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="topbar">
      <div class="brand">
        {LOGO_SVG}
        Siren Tracker
        <span class="brand-sub">NAVAL INTELLIGENCE v2.4</span>
      </div>
    </div>
    <style>
    div[data-testid="stHorizontalBlock"]{{gap:0!important;background:var(--surface);border-bottom:1px solid var(--border);padding:4px 28px!important;margin-top:-4px!important}}
    div[data-testid="stHorizontalBlock"]>div[data-testid="column"]{{padding:0!important;flex:0 0 auto!important;width:auto!important;min-width:0!important}}
    div[data-testid="stHorizontalBlock"] [data-testid="baseButton-secondary"]{{background:transparent!important;border:none!important;box-shadow:none!important;padding:6px 11px!important;border-radius:8px!important;font-size:13px!important;font-weight:500!important;color:#606060!important;white-space:nowrap!important;transform:none!important}}
    div[data-testid="stHorizontalBlock"] [data-testid="baseButton-secondary"]:hover{{background:#F2F5FA!important;color:#0B3954!important;transform:none!important;box-shadow:none!important}}
    div[data-testid="stHorizontalBlock"] [data-testid="baseButton-secondary"]:active,
    div[data-testid="stHorizontalBlock"] [data-testid="baseButton-secondary"]:focus{{transform:none!important;box-shadow:none!important;outline:none!important}}
    .nav-ativo [data-testid="baseButton-secondary"]{{background:#EEF2FF!important;color:#4379EE!important}}
    div[data-testid="stHorizontalBlock"] .stMarkdown{{display:none!important}}
    </style>
    """, unsafe_allow_html=True)

    cols = st.columns(len(PAGES) + 2)
    for i, (key, label) in enumerate(PAGES):
        with cols[i]:
            if key == pagina_ativa:
                st.markdown('<div class="nav-ativo">', unsafe_allow_html=True)
            if st.button(label, key=f"_nav_{key}"):
                st.session_state["_nav_target"] = key
                st.rerun()
            if key == pagina_ativa:
                st.markdown("</div>", unsafe_allow_html=True)
    with cols[len(PAGES)]:
        st.button("🔒 Detector", key="_nav_locked_1", disabled=True)
    with cols[len(PAGES)+1]:
        st.button("🔒 Avistamentos", key="_nav_locked_2", disabled=True)


def sonar_html():
    return """
    <div class="sonar-widget">
      <div class="sonar-title">SONAR — VARREDURA ATIVA · ATLÂNTICO</div>
      <div style="position:relative;height:180px;display:flex;align-items:center;justify-content:center;">
        <div style="position:absolute;border-radius:50%;border:1px solid rgba(46,184,172,.3);animation:sp 3s ease-out infinite;width:170px;height:170px"></div>
        <div style="position:absolute;border-radius:50%;border:1px solid rgba(46,184,172,.3);animation:sp 3s ease-out .7s infinite;width:120px;height:120px"></div>
        <div style="position:absolute;border-radius:50%;border:1px solid rgba(46,184,172,.3);animation:sp 3s ease-out 1.4s infinite;width:70px;height:70px"></div>
        <div style="width:8px;height:8px;border-radius:50%;background:#2EB8AC;position:absolute;z-index:5"></div>
        <div style="position:absolute;width:92px;height:2px;background:linear-gradient(to right,rgba(46,184,172,.15),rgba(46,184,172,.8));transform-origin:left center;animation:sc 4s linear infinite;left:50%;top:50%"></div>
        <div style="position:absolute;top:28%;left:58%;width:6px;height:6px;border-radius:50%;background:#A43955;box-shadow:0 0 8px #A43955"></div>
        <div style="position:absolute;top:33%;left:63%;width:6px;height:6px;border-radius:50%;background:#A43955;box-shadow:0 0 8px #A43955"></div>
        <div style="position:absolute;top:68%;left:38%;width:6px;height:6px;border-radius:50%;background:#F39237;box-shadow:0 0 6px #F39237"></div>
        <div style="position:absolute;top:53%;left:73%;width:6px;height:6px;border-radius:50%;background:#2EB8AC;box-shadow:0 0 6px #2EB8AC"></div>
      </div>
      <style>
        @keyframes sp{0%{transform:scale(.1);opacity:.8}100%{transform:scale(1);opacity:0}}
        @keyframes sc{from{transform:rotate(0)}to{transform:rotate(360deg)}}
      </style>
      <div style="display:flex;gap:12px;margin-top:6px">
        <div style="display:flex;align-items:center;gap:5px;font-size:11px;color:#8E9DCC"><div style="width:8px;height:8px;border-radius:50%;background:#A43955"></div>Alto</div>
        <div style="display:flex;align-items:center;gap:5px;font-size:11px;color:#8E9DCC"><div style="width:8px;height:8px;border-radius:50%;background:#F39237"></div>Médio</div>
        <div style="display:flex;align-items:center;gap:5px;font-size:11px;color:#8E9DCC"><div style="width:8px;height:8px;border-radius:50%;background:#2EB8AC"></div>Baixo</div>
      </div>
    </div>"""
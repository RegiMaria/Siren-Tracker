import streamlit as st

st.set_page_config(
    page_title="Siren Tracker — Naval Intelligence",
    page_icon="🧜",
    layout="wide",
    initial_sidebar_state="collapsed",
)

import pages.dashboard    as dashboard
import pages.mapa         as mapa
import pages.intel        as intel
import pages.encyclopedia as encyclopedia
import pages.routes       as routes
import pages.reports      as reports

# ── define as páginas como objetos ───────────────────────────────────────────
PAGE_DASHBOARD    = st.Page(dashboard.run,    title="Dashboard",     icon="🗺️", url_path="dashboard")
PAGE_MAPA         = st.Page(mapa.run,         title="Mapa",          icon="📍", url_path="mapa")
PAGE_INTEL        = st.Page(intel.run,        title="Inteligência",  icon="📡", url_path="intel")
PAGE_ENCYCLOPEDIA = st.Page(encyclopedia.run, title="Enciclopédia",  icon="📖", url_path="encyclopedia")
PAGE_ROUTES       = st.Page(routes.run,       title="Rotas",         icon="🧭", url_path="routes")
PAGE_REPORTS      = st.Page(reports.run,      title="Relatórios",    icon="📋", url_path="reports")

# ── mapa de chave → objeto de página ─────────────────────────────────────────
PAGES_MAP = {
    "dashboard":    PAGE_DASHBOARD,
    "mapa":         PAGE_MAPA,
    "intel":        PAGE_INTEL,
    "encyclopedia": PAGE_ENCYCLOPEDIA,
    "routes":       PAGE_ROUTES,
    "reports":      PAGE_REPORTS,
}

# ── intercepta cliques da topbar e navega sem abrir nova aba ──────────────────
if "_nav_target" in st.session_state:
    target_key = st.session_state.pop("_nav_target")
    target_page = PAGES_MAP.get(target_key)
    if target_page:
        st.switch_page(target_page)

# ── registra navegação ────────────────────────────────────────────────────────
pg = st.navigation(
    pages=list(PAGES_MAP.values()),
    position="hidden",
)
pg.run()
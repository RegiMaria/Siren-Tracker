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

PAGES_MAP = {
    "dashboard":    st.Page(dashboard.run,    title="Dashboard",    icon="🗺️", url_path="dashboard"),
    "mapa":         st.Page(mapa.run,         title="Mapa",         icon="📍", url_path="mapa"),
    "intel":        st.Page(intel.run,        title="Inteligência", icon="📡", url_path="intel"),
    "encyclopedia": st.Page(encyclopedia.run, title="Enciclopédia", icon="📖", url_path="encyclopedia"),
    "routes":       st.Page(routes.run,       title="Rotas",        icon="🧭", url_path="routes"),
    "reports":      st.Page(reports.run,      title="Relatórios",   icon="📋", url_path="reports"),
}

# intercepta clique da topbar — navega com objeto st.Page (não URL) # Nova alteração aqui
if "_nav_target" in st.session_state:
    target_key = st.session_state.pop("_nav_target")
    target_page = PAGES_MAP.get(target_key)
    if target_page:
        st.switch_page(target_page)

pg = st.navigation(pages=list(PAGES_MAP.values()), position="hidden")
pg.run()
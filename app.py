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

pg = st.navigation(
    pages=[
        st.Page(dashboard.run,    title="Dashboard",     icon="🗺️", url_path="dashboard"),
        st.Page(mapa.run,         title="Mapa",          icon="📍", url_path="mapa"),
        st.Page(intel.run,        title="Inteligência",  icon="📡", url_path="intel"),
        st.Page(encyclopedia.run, title="Enciclopédia",  icon="📖", url_path="encyclopedia"),
        st.Page(routes.run,       title="Rotas",         icon="🧭", url_path="routes"),
        st.Page(reports.run,      title="Relatórios",    icon="📋", url_path="reports"),
    ],
    position="hidden",
)
pg.run()

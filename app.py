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

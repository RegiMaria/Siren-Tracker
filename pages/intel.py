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

    st.markdown("</div>", unsafe_allow_html=True)

"""Entry point — Streamlit multi-page router."""
import streamlit as st

st.set_page_config(
    page_title="PV Manufacturing Control System",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

with st.sidebar:
    st.toggle("🌙 Dark mode", key="dark_mode")

pg = st.navigation([
    st.Page("pages/introduction.py",      title="Introduction",        icon="📑", url_path="introduction"),
    st.Page("pages/pv_stages.py",         title="PV Stages",           icon="🏭", url_path="pv_stages"),
    st.Page("home.py",                    title="Live Demo",            icon="☀️", default=True),
    st.Page("pages/synthetic_data.py",    title="Synthetic Data",      icon="📊", url_path="synthetic_data"),
    st.Page("pages/sk_explainer.py",      title="How SK Works",        icon="⚙️", url_path="sk_explainer"),
    st.Page("pages/agents_config.py",     title="Agents Config",       icon="🤖", url_path="agents_config"),
])
pg.run()

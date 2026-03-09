import streamlit as st
from fast_learning import run_fast_learning
from normal_trading import run_normal_trading

st.set_page_config(page_title="AI Stock Teaching Agent", layout="wide")

st.sidebar.title("Trading Mode")

mode = st.sidebar.radio(
    "Choose Mode",
    ["Fast Learning", "Normal Trading"]
)

if mode == "Fast Learning":
    run_fast_learning()

elif mode == "Normal Trading":
    run_normal_trading()
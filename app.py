import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="SBBT Proposal Engine", layout="centered")

# --- SAFE MATRIX LOADER ---
@st.cache_data
def load_sbbt_matrix():
    file_name = "SBBT_Master_Quotation_Matrix.xlsx"
    if not os.path.exists(file_name):
        return None
    try:
        df = pd.read_excel(file_name, sheet_name="AI Master Matrix")
        return df
    except Exception as e:
        return None

df_matrix = load_sbbt_matrix()

# --- LOGIN GATEWAY ---
if 'authenticated' not in st.session_state: st.session_state['authenticated'] = False
if not st.session_state['authenticated']:
    if st.button("Login (Admin)"):
        st.session_state['authenticated'] = True
        st.rerun()
    st.stop()

# --- MAIN ENGINE (Yahan apna logic rakhein) ---
st.write("Engine Loaded Successfully")

# (Aapka baki pura code yahan aayega...)

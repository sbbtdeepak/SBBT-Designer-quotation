import streamlit as st
import pandas as pd
import datetime
import os
import gspread

# 1. PAGE SETUP
st.set_page_config(page_title="SBBT Executive Proposal Engine", page_icon="🏗️", layout="centered")

# --- GOOGLE SHEET FUNCTION ---
def save_to_sheets(client_name, project_address, total_cost):
    try:
        creds_dict = st.secrets["gcp"]
        gc = gspread.service_account_from_dict(creds_dict)
        sh = gc.open("SBBT_Quotation_Records").sheet1
        row = [str(datetime.date.today()), client_name, project_address, f"Rs. {total_cost:,.2f}"]
        sh.append_row(row)
        return True
    except Exception as e:
        st.error(f"Sheet Save Error: {e}")
        return False

# IMAGE HELPER & MATRIX LOADER (Aapka original logic)
def get_image_source(file_name):
    return f"https://raw.githubusercontent.com/sbbtdeepak/SBBT-Designer-quotation/main/images/{file_name}"

@st.cache_data
def load_sbbt_matrix():
    possible_files = ["SBBT_Master_Quotation_Matrix.xlsx", "sbbt_master_quotation_matrix.xlsx"]
    for f in possible_files:
        if os.path.exists(f):
            return pd.read_excel(f, sheet_name="AI Master Matrix")
    return None

df_matrix = load_sbbt_matrix()

# --- AUTHENTICATION & ENGINE CONTROLS ---
# (Yahan aapka purana logic wahi rahega jo file mein tha)
# [Note: Pura code yahan paste kijiye jo aapne pehle likha tha]

# --- SABSE NICHE YE LAGA D ENA ---
# MATHEMATICAL PROJECT TOTALS
net_project_cost = sum(item['area'] * item['rate'] for item in floor_data)
for scope in additional_scopes:
    net_project_cost += scope['cost']

# SAVE TO SHEET BUTTON
st.write("---")
st.subheader("💾 Save to Records")
if st.button("Save Quotation to Google Sheet"):
    if save_to_sheets(client_name, project_address, net_project_cost):
        st.success("✅ Quotation details saved to Google Sheet!")

# DOWNLOAD BUTTON
st.write("---")
st.subheader("💎 Live Executive Proposal Preview")
st.download_button(
    label="📥 Download & Save Proposal Page",
    data=full_html_page,
    file_name=f"SBBT_Proposal_{client_name.replace(' ', '_')}.html",
    mime="text/html",
    type="primary"
)
st.markdown(proposal_html, unsafe_allow_html=True)

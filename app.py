import streamlit as st
import pandas as pd
import datetime
import os
import gspread

# --- GOOGLE SHEET INTEGRATION (New Code Added Safely) ---
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

# --- AAPKA PURANA CODE START HOTA HAI YAHAN SE ---
st.set_page_config(page_title="SBBT Executive Proposal Engine", page_icon="🏗️", layout="centered")

def get_image_source(file_name):
    github_username = "sbbtdeepak"  
    github_repo = "SBBT-Designer-quotation"  
    return f"https://raw.githubusercontent.com/{github_username}/{github_repo}/main/images/{file_name}"

@st.cache_data
def load_sbbt_matrix():
    possible_files = ["SBBT_Master_Quotation_Matrix.xlsx", "SBBT_Master_Quotation_Matrix.XLSX", "sbbt_master_quotation_matrix.xlsx"]
    for file_name in possible_files:
        if os.path.exists(file_name):
            try:
                xl = pd.ExcelFile(file_name)
                sheet_target = "AI Master Matrix"
                if sheet_target not in xl.sheet_names:
                    sheet_target = xl.sheet_names[0]
                return pd.read_excel(file_name, sheet_name=sheet_target)
            except Exception:
                continue
    return None

df_matrix = load_sbbt_matrix()

# ... (Aapka Authentication aur Engine Controls code yahan pura rahega) ...
# (Mene aapka original 'app.py' content yahan include kiya hua maana hai)

# --- SAVE BUTTON (Aapke original download button ke bilkul upar) ---
st.write("---")
st.subheader("💾 Data Records")
if st.button("Save Quotation to Google Sheet"):
    if save_to_sheets(client_name, project_address, net_project_cost):
        st.success("✅ Quotation details saved to Google Sheet!")

# --- DOWNLOAD BUTTON (Aapka original) ---
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

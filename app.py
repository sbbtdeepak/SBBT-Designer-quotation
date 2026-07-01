import streamlit as st
import pandas as pd
import datetime
import os

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="SBBT Executive Proposal Engine", page_icon="🏗️", layout="centered")

# --- 2. IMAGE HELPER ---
def get_image_source(file_name):
    return f"https://raw.githubusercontent.com/sbbtdeepak/SBBT-Designer-quotation/main/images/{file_name}"

# --- 3. MATRIX LOADER (Jaisa pehle tha) ---
@st.cache_data
def load_sbbt_matrix():
    possible_files = ["SBBT_Master_Quotation_Matrix.xlsx", "SBBT_Master_Quotation_Matrix.XLSX", "sbbt_master_quotation_matrix.xlsx"]
    for file_name in possible_files:
        if os.path.exists(file_name):
            try:
                xl = pd.ExcelFile(file_name)
                sheet_target = "AI Master Matrix"
                if sheet_target not in xl.sheet_names: sheet_target = xl.sheet_names[0]
                return pd.read_excel(file_name, sheet_name=sheet_target)
            except: continue
    return None

df_matrix = load_sbbt_matrix()

# --- 4. AUTHENTICATION & ENGINE (Aapka original logic) ---
if 'authenticated' not in st.session_state: st.session_state['authenticated'] = False
if not st.session_state['authenticated']:
    # [Aapka original login code yahan waisa ka waisa rahega]
    st.title("🏗️ SBBT Enterprise Portal")
    # ... (Login logic) ...
    st.stop()

# --- 5. CALCULATIONS (Aapka original code) ---
# [Floor data, Additional scope, Total Cost calculation wahi rahega]

# --- 6. MILESTONE MATRIX (Ise PDF generation se just pehle generate karein) ---
milestone_html = ""
if final_ok_switch: # Aapka original switch variable
    milestone_html = f"""
    <div style="margin-top: 50px; padding: 20px; border: 2px solid #2563eb; border-radius: 10px; background: #eff6ff;">
        <h3>💳 Payment Milestone Matrix</h3>
        <p>Total Estimated: <b>Rs. {net_project_cost:,.2f}</b></p>
        <ul>
            <li>Structure Stage: 40%</li>
            <li>Finishing Stage: 40%</li>
            <li>Handover: 20%</li>
        </ul>
    </div>
    """

# --- 7. PROPOSAL HTML ASSEMBLY (Milestone ko niche add kiya) ---
proposal_html = f"""
<div style="font-family: sans-serif; padding: 20px;">
    <h1>SBBT Executive Proposal</h1>
    {milestone_html}
    
    </div>
"""

# --- 8. DOWNLOAD & PREVIEW (Original) ---
st.download_button("📥 Download Proposal", proposal_html, "Proposal.html", "text/html")
st.markdown(proposal_html, unsafe_allow_html=True)

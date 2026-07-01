import streamlit as st
import pandas as pd
import datetime
import os

# 1. PAGE SETUP
st.set_page_config(page_title="SBBT Proposal Engine", layout="centered")

# 2. SAFE MATRIX LOADER (Crash nahi hoga)
@st.cache_data
def load_sbbt_matrix():
    file_name = "SBBT_Master_Quotation_Matrix.xlsx"
    if not os.path.exists(file_name):
        return None
    try:
        # Pura data read karein
        df = pd.read_excel(file_name, sheet_name="AI Master Matrix")
        return df
    except:
        return None

df_matrix = load_sbbt_matrix()

# 3. AUTHENTICATION GATEWAY
if 'authenticated' not in st.session_state: st.session_state['authenticated'] = False
if not st.session_state['authenticated']:
    st.title("🏗️ SBBT Enterprise Login")
    if st.button("Enter Portal"):
        st.session_state['authenticated'] = True
        st.rerun()
    st.stop()

# --- ENGINE LOGIC START ---
# (Yahan apna purana 'Engine Controls', 'Floor Area' inputs wahi rakhein)
# ...

# 4. DYNAMIC SPECIFICATION TABLE (Safely)
spec_table_html = "<p>Data not loaded from Excel.</p>"
if df_matrix is not None:
    # Column name match hona chahiye
    package_col = selected_excel_col # 'Premium Luxury Package' etc
    if package_col in df_matrix.columns:
        table_rows = "".join([f"<tr><td style='border:1px solid #ddd; padding:8px;'>{row.get('Category / Element', '')}</td><td style='border:1px solid #ddd; padding:8px;'>{row.get(package_col, '')}</td></tr>" for _, row in df_matrix.iterrows()])
        spec_table_html = f"<table style='width:100%; border-collapse:collapse;'>{table_rows}</table>"

# 5. MILESTONE MATRIX (BILKUL NICHE)
milestone_html = f"""
<div style="margin-top: 50px; padding: 20px; border: 2px solid #2563eb; border-radius: 10px; background: #eff6ff;">
    <h3>💳 Payment Milestone Matrix</h3>
    <p>Total Estimated: <b>Rs. {net_project_cost:,.2f}</b></p>
    <ul>
        <li>Structure: 40% | Finishing: 40% | Handover: 20%</li>
    </ul>
</div>
"""

# 6. HTML ASSEMBLY
proposal_html = f"""
<div style="font-family: Arial;">
    <h1>Proposal for {client_name}</h1>
    <h2>Specifications</h2>
    {spec_table_html}
    {milestone_html}
</div>
"""

# 7. DOWNLOAD & PREVIEW
st.download_button("📥 Download Proposal", proposal_html, "SBBT_Proposal.html", "text/html")
st.markdown(proposal_html, unsafe_allow_html=True)

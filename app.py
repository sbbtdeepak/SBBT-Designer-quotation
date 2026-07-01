import streamlit as st
import pandas as pd
import datetime
import os

# 1. PAGE SETUP
st.set_page_config(page_title="SBBT Executive Proposal Engine", page_icon="🏗️", layout="centered")

# 2. ROBUST MATRIX LOADER
@st.cache_data
def load_sbbt_matrix():
    file_name = "SBBT_Master_Quotation_Matrix.xlsx"
    if not os.path.exists(file_name):
        return None
    try:
        raw_df = pd.read_excel(file_name, sheet_name="AI Master Matrix", header=None)
        header_row = 0
        for i, row in raw_df.iterrows():
            if "Category / Element" in row.astype(str).values:
                header_row = i
                break
        df = pd.read_excel(file_name, sheet_name="AI Master Matrix", header=header_row)
        return df
    except Exception:
        return None

df_matrix = load_sbbt_matrix()

# --- [YAHA APNA AUTHENTICATION AUR ENGINE CONTROLS WALA CODE RAKHEIN] ---
# (Yahan user inputs: client_name, floor_data, additional_scopes, selected_excel_col etc. define honge)

# 3. DYNAMIC SPECIFICATION TABLE GENERATOR
def generate_spec_table(df, package_col):
    if df is None: return "<p>Specs Matrix missing.</p>"
    table_html = "<table style='width:100%; border-collapse: collapse; margin-top:20px;'>"
    table_html += "<tr style='background:#f3f4f6;'><th>Category</th><th>Specifications</th></tr>"
    for _, row in df.iterrows():
        table_html += f"<tr><td style='border:1px solid #ddd; padding:8px;'>{row.get('Category / Element', '')}</td>"
        table_html += f"<td style='border:1px solid #ddd; padding:8px;'>{row.get(package_col, 'Standard')}</td></tr>"
    table_html += "</table>"
    return table_html

spec_table_html = generate_spec_table(df_matrix, selected_excel_col)

# 4. MILESTONE MATRIX (SABSE NICHE KE LIYE)
milestone_html = f"""
<div style="margin-top: 40px; padding: 20px; border: 2px solid #2563eb; border-radius: 10px; background: #eff6ff;">
    <h3 style="color: #1e3a8a; margin-top: 0;">💳 Smart Stage Billing Milestone Matrix</h3>
    <p>Total Estimated Cost: <b>Rs. {net_project_cost:,.2f}</b></p>
    <table style="width:100%; border-collapse: collapse;">
        <tr><td style="padding:5px;">Structure Stage</td><td>40%</td></tr>
        <tr><td style="padding:5px;">Finishing Stage</td><td>40%</td></tr>
        <tr><td style="padding:5px;">Handover</td><td>20%</td></tr>
    </table>
</div>
"""

# 5. PROPOSAL HTML ASSEMBLY (Yahan sab combine hoga)
proposal_html = f"""
<div style="font-family: Arial, sans-serif; padding: 20px;">
    <h1>SBBT Proposal for {client_name}</h1>
    {spec_table_html}
    {milestone_html} 
    </div>
"""

# 6. DOWNLOAD & DISPLAY
st.download_button("📥 Download PDF Proposal", proposal_html, "Proposal.html", "text/html")
st.markdown(proposal_html, unsafe_allow_html=True)

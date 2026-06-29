import streamlit as st
import pandas as pd
import datetime
import os

# 1. PAGE SETUP
st.set_page_config(page_title="SBBT Executive Proposal Engine", page_icon="🏗️", layout="centered")

def get_image_source(file_name):
    github_username = "sbbtdeepak"  
    github_repo = "SBBT-Designer-quotation"  
    return f"https://raw.githubusercontent.com/{github_username}/{github_repo}/main/images/{file_name}"

# 2. MATRIX LOADER
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

# 3. AUTH & CONTROLS
if 'authenticated' not in st.session_state: st.session_state['authenticated'] = False
if not st.session_state['authenticated']:
    st.title("🏗️ SBBT Enterprise Portal")
    if st.text_input("Password", type="password") == "sbbt@2026":
        if st.button("Authenticate"): st.session_state['authenticated'] = True; st.rerun()
    st.stop()

# INPUTS
package_options = {"Solid Structure Core": "Core Shell Package", "Essential Finishing": "Essential Package", "Premium Luxury Profile": "Premium Luxury Package"}
col1, col2 = st.columns(2)
with col1:
    client_name = st.text_input("Client Name", "Mr. & Mrs. Sharma")
    project_address = st.text_input("Site Location", "Palam, Gurgaon (HR)")
    selected_global_display = st.selectbox("Select Master Package", list(package_options.keys()), index=2)
    selected_excel_col = package_options[selected_global_display]
with col2:
    plot_area_yd = st.number_input("Plot Area (Sq. Yards)", value=100)
    total_floors = st.slider("Number of Floors", 1, 12, 4)

# FLOOR & MILESTONE CALCULATION (Original Logic)
floor_data = []
net_project_cost = 0
for i in range(total_floors):
    f_area = st.number_input(f"Area Floor {i}", value=900)
    f_rate = st.number_input(f"Rate Floor {i}", value=1700)
    floor_data.append({"floor": f"Floor {i}", "area": f_area, "rate": f_rate, "layout": "Standard"})
    net_project_cost += (f_area * f_rate)

final_ok_switch = st.toggle("🔒 SHOW MILESTONE PAYMENT MATRIX", value=True)

# IMAGE MAPPING (Updated)
if "Essential" in selected_global_display:
    img_list = [{"title": "Essential Elevation", "file": "elevation_essential.jpg"}, {"title": "Pop Cornice Styling", "file": "pop_cornice.jpg"}]
else:
    img_list = [{"title": "HPL Cladding", "file": "hpl_cladding.jpg"}] # Premium logic here

images_html = "".join([f"<img src='{get_image_source(i['file'])}' width='100'>" for i in img_list])
milestone_section_html = "<div style='border:1px solid #ccc; padding:20px;'><h3>💳 Payment Matrix</h3></div>" if final_ok_switch else ""

# PROPOSAL ASSEMBLY (Milestone moved below Commercial Terms)
proposal_html = f"""
<div style="padding:40px;">
    <h1>SBBT PROPOSAL</h1>
    <p>Client: {client_name}</p>
    
    <div>{images_html}</div>

    <div style="margin-top:40px;">
        <h3>🛡️ 7. Commercial Execution Terms</h3>
        <p>Validity: 30 Days.</p>
    </div>

    {milestone_section_html}
    
    <div style="margin-top:20px;"><b>Signature of Executive Authority</b></div>
</div>
"""

# DOWNLOAD & DISPLAY
st.download_button("📥 Download Proposal", data=proposal_html, file_name="proposal.html", mime="text/html")
st.markdown(proposal_html, unsafe_allow_html=True)
